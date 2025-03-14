from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from supabase import Client

from app.core.deps import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.schemas.verification import (
    VerificationRequestCreate, VerificationRequestUpdate,
    VerificationRequestResponse, VerificationStats,
    VerificationRequestStatus, VerificationType,
    DocumentUpload, VerificationDashboard,
    BatchDocumentUpload, DocumentValidation
)
from app.services.verification import VerificationService

router = APIRouter()

@router.post("/requests", response_model=VerificationRequestResponse)
async def create_verification_request(
    request: VerificationRequestCreate,
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create a new verification request.
    """
    return await VerificationService.create_verification_request(db, current_user, request)

@router.get("/requests/{request_id}", response_model=VerificationRequestResponse)
async def get_verification_request(
    request_id: str,
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a verification request by ID.
    """
    request = await VerificationService.get_verification_request(db, request_id)
    if not request:
        raise HTTPException(
            status_code=404,
            detail="Verification request not found",
        )
    
    # Only allow users to view their own requests unless they're an admin
    if not current_user.is_superuser and request.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    
    return request

@router.get("/requests", response_model=List[VerificationRequestResponse])
async def get_user_verification_requests(
    status: Optional[VerificationRequestStatus] = None,
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get all verification requests for the current user.
    """
    return await VerificationService.get_user_verification_requests(db, current_user.id, status)

@router.put("/requests/{request_id}", response_model=VerificationRequestResponse)
async def update_verification_request(
    request_id: str,
    update: VerificationRequestUpdate,
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a verification request (admin only).
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    
    request = await VerificationService.get_verification_request(db, request_id)
    if not request:
        raise HTTPException(
            status_code=404,
            detail="Verification request not found",
        )
    
    return await VerificationService.update_verification_request(
        db,
        request_id,
        update,
        current_user.id
    )

@router.get("/stats", response_model=VerificationStats)
async def get_verification_stats(
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get verification statistics (admin only).
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    
    return await VerificationService.get_verification_stats(db)

@router.get("/types", response_model=List[str])
async def get_verification_types() -> Any:
    """
    Get all available verification types.
    """
    return [t.value for t in VerificationType]

@router.post("/requests/{request_id}/documents", response_model=DocumentUpload)
async def upload_verification_document(
    request_id: str,
    file: UploadFile = File(...),
    document_type: str = Form(...),
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Upload a document for verification evidence.
    """
    # Check if request exists and belongs to user
    request = await VerificationService.get_verification_request(db, request_id)
    if not request:
        raise HTTPException(
            status_code=404,
            detail="Verification request not found",
        )
    
    if not current_user.is_superuser and request.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    
    # Check if request is still pending
    if request.status != VerificationRequestStatus.PENDING:
        raise HTTPException(
            status_code=400,
            detail="Cannot upload documents for non-pending requests",
        )
    
    return await VerificationService.upload_document(
        db,
        file,
        document_type,
        current_user.id,
        request_id
    )

@router.get("/dashboard", response_model=VerificationDashboard)
async def get_verification_dashboard(
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get verification dashboard data (admin only).
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    
    return await VerificationService.get_dashboard_data(db)

@router.get("/requests/{request_id}/documents", response_model=List[DocumentUpload])
async def get_verification_documents(
    request_id: str,
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get all documents for a verification request.
    """
    # Check if request exists and belongs to user
    request = await VerificationService.get_verification_request(db, request_id)
    if not request:
        raise HTTPException(
            status_code=404,
            detail="Verification request not found",
        )
    
    if not current_user.is_superuser and request.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    
    # Get documents
    response = await db.table("verification_documents").select("*").eq("request_id", request_id).execute()
    return [DocumentUpload(**item) for item in response.data]

@router.delete("/requests/{request_id}/documents/{document_id}")
async def delete_verification_document(
    request_id: str,
    document_id: str,
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete a verification document.
    """
    # Check if request exists and belongs to user
    request = await VerificationService.get_verification_request(db, request_id)
    if not request:
        raise HTTPException(
            status_code=404,
            detail="Verification request not found",
        )
    
    if not current_user.is_superuser and request.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    
    # Check if document exists
    document_response = await db.table("verification_documents").select("*").eq("id", document_id).execute()
    if not document_response.data:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )
    
    # Delete document from storage
    document = document_response.data[0]
    await VerificationService._delete_from_storage(document["file_url"])
    
    # Delete document record
    await db.table("verification_documents").delete().eq("id", document_id).execute()
    
    return {"message": "Document deleted successfully"}

@router.post("/requests/{request_id}/documents/batch", response_model=BatchDocumentUpload)
async def batch_upload_verification_documents(
    request_id: str,
    files: List[UploadFile] = File(...),
    document_type: str = Form(...),
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Upload multiple documents for verification evidence in a batch.
    """
    # Check if request exists and belongs to user
    request = await VerificationService.get_verification_request(db, request_id)
    if not request:
        raise HTTPException(
            status_code=404,
            detail="Verification request not found",
        )
    
    if not current_user.is_superuser and request.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    
    # Check if request is still pending
    if request.status != VerificationRequestStatus.PENDING:
        raise HTTPException(
            status_code=400,
            detail="Cannot upload documents for non-pending requests",
        )
    
    return await VerificationService.batch_upload_documents(
        db,
        files,
        document_type,
        current_user.id,
        request_id
    )

@router.post("/documents/validate", response_model=DocumentValidation)
async def validate_document(
    file: UploadFile = File(...),
    document_type: str = Form(...),
) -> Any:
    """
    Validate a document before upload.
    """
    return await VerificationService.validate_document(file, document_type)

@router.get("/dashboard/visualizations", response_model=Dict[str, Any])
async def get_dashboard_visualizations(
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get enhanced dashboard visualizations (admin only).
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    
    # Get basic dashboard data
    dashboard_data = await VerificationService.get_dashboard_data(db)
    
    # Get additional visualizations
    visualizations = {
        "verification_trends": {
            "daily": await VerificationService.get_daily_verification_trends(db),
            "weekly": await VerificationService.get_weekly_verification_trends(db),
            "monthly": dashboard_data.monthly_trends
        },
        "document_statistics": {
            "by_type": await VerificationService.get_document_type_statistics(db),
            "by_size": await VerificationService.get_document_size_statistics(db),
            "validation_success_rate": await VerificationService.get_document_validation_success_rate(db)
        },
        "reviewer_performance": {
            "top_reviewers": dashboard_data.top_reviewers,
            "average_response_time": dashboard_data.average_response_time,
            "reviewer_activity": await VerificationService.get_reviewer_activity(db)
        },
        "verification_metrics": {
            "completion_rate": dashboard_data.completion_rate,
            "rejection_rate": dashboard_data.rejection_rate,
            "average_verification_time": await VerificationService.get_average_verification_time(db),
            "verification_success_rate": await VerificationService.get_verification_success_rate(db)
        }
    }
    
    return visualizations 