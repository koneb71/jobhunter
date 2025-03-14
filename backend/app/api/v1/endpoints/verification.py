from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import and_, desc, func, or_
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user
from app.core.deps import get_db
from app.models.user import User
from app.schemas.verification import (
    BatchDocumentUpload,
    DocumentUpload,
    DocumentValidation,
    VerificationDashboard,
    VerificationRequestCreate,
    VerificationRequestResponse,
    VerificationRequestStatus,
    VerificationRequestUpdate,
    VerificationStats,
    VerificationType,
)
from app.services.verification import VerificationService

router = APIRouter()


@router.post("/requests", response_model=VerificationRequestResponse)
async def create_verification_request(
    request: VerificationRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create a new verification request.
    """
    return await VerificationService.create_verification_request(
        db, current_user, request
    )


@router.get("/requests/{request_id}", response_model=VerificationRequestResponse)
async def get_verification_request(
    request_id: str,
    db: Session = Depends(get_db),
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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get all verification requests for the current user.
    """
    return await VerificationService.get_user_verification_requests(
        db, current_user.id, status
    )


@router.put("/requests/{request_id}", response_model=VerificationRequestResponse)
async def update_verification_request(
    request_id: str,
    update: VerificationRequestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a verification request.
    """
    # Check if request exists
    request = await VerificationService.get_verification_request(db, request_id)
    if not request:
        raise HTTPException(
            status_code=404,
            detail="Verification request not found",
        )

    # Only allow admins to update requests
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )

    return await VerificationService.update_verification_request(
        db, request_id, update, current_user.id
    )


@router.get("/stats", response_model=VerificationStats)
async def get_verification_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get verification statistics.
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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Upload a document for a verification request.
    """
    # Check if request exists
    request = await VerificationService.get_verification_request(db, request_id)
    if not request:
        raise HTTPException(
            status_code=404,
            detail="Verification request not found",
        )

    # Check permissions
    if not current_user.is_superuser and request.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )

    # Check if request is in a state that allows document uploads
    if request.status not in [
        VerificationRequestStatus.PENDING,
        VerificationRequestStatus.IN_REVIEW,
    ]:
        raise HTTPException(
            status_code=400,
            detail="Cannot upload documents for requests that are not pending or in review",
        )

    try:
        return await VerificationService.upload_document(
            db, request_id, file, document_type
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/dashboard", response_model=VerificationDashboard)
async def get_verification_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get verification dashboard data.
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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get all documents for a verification request.
    """
    # Check if request exists
    request = await VerificationService.get_verification_request(db, request_id)
    if not request:
        raise HTTPException(
            status_code=404,
            detail="Verification request not found",
        )

    # Check permissions
    if not current_user.is_superuser and request.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )

    return await VerificationService.get_request_documents(db, request_id)


@router.delete("/requests/{request_id}/documents/{document_id}")
async def delete_verification_document(
    request_id: str,
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete a document from a verification request.
    """
    # Check if request exists
    request = await VerificationService.get_verification_request(db, request_id)
    if not request:
        raise HTTPException(
            status_code=404,
            detail="Verification request not found",
        )

    # Check permissions
    if not current_user.is_superuser and request.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )

    # Check if request is in a state that allows document deletion
    if request.status not in [
        VerificationRequestStatus.PENDING,
        VerificationRequestStatus.IN_REVIEW,
    ]:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete documents from requests that are not pending or in review",
        )

    try:
        await VerificationService.delete_document(db, request_id, document_id)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post(
    "/requests/{request_id}/documents/batch", response_model=BatchDocumentUpload
)
async def batch_upload_verification_documents(
    request_id: str,
    files: List[UploadFile] = File(...),
    document_type: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Upload multiple documents for a verification request.
    """
    # Check if request exists
    request = await VerificationService.get_verification_request(db, request_id)
    if not request:
        raise HTTPException(
            status_code=404,
            detail="Verification request not found",
        )

    # Check permissions
    if not current_user.is_superuser and request.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )

    # Check if request is in a state that allows document uploads
    if request.status not in [
        VerificationRequestStatus.PENDING,
        VerificationRequestStatus.IN_REVIEW,
    ]:
        raise HTTPException(
            status_code=400,
            detail="Cannot upload documents for requests that are not pending or in review",
        )

    try:
        return await VerificationService.batch_upload_documents(
            db, files, document_type
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get data for dashboard visualizations.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )

    # Get verification trends
    daily_trends = await VerificationService.get_daily_verification_trends(db)
    weekly_trends = await VerificationService.get_weekly_verification_trends(db)

    # Get document statistics
    document_stats = await VerificationService.get_document_type_statistics(db)
    document_sizes = await VerificationService.get_document_size_statistics(db)
    validation_stats = await VerificationService.get_document_validation_success_rate(
        db
    )

    # Get reviewer activity
    reviewer_activity = await VerificationService.get_reviewer_activity(db)

    # Get overall metrics
    avg_verification_time = await VerificationService.get_average_verification_time(db)
    success_rate = await VerificationService.get_verification_success_rate(db)

    return {
        "trends": {
            "daily": daily_trends,
            "weekly": weekly_trends,
        },
        "documents": {
            "by_type": document_stats,
            "sizes": document_sizes,
            "validation": validation_stats,
        },
        "reviewers": reviewer_activity,
        "metrics": {
            "average_verification_time": avg_verification_time,
            "success_rate": success_rate,
        },
    }
