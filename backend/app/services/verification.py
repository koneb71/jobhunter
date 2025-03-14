from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
from supabase import Client
import aiofiles
import os
from fastapi import UploadFile
from app.core.config import settings
from app.core.email import send_email
from app.schemas.verification import (
    VerificationRequest, VerificationRequestCreate,
    VerificationRequestUpdate, VerificationRequestResponse,
    VerificationStats, VerificationRequestStatus,
    VerificationType, DocumentUpload, VerificationEvidence,
    VerificationNotification, VerificationDashboard,
    DocumentValidation, DocumentValidationError,
    BatchDocumentUpload, MAX_FILE_SIZE, ALLOWED_MIME_TYPES
)
from app.schemas.profile import ProfileVerification, ProfileVerificationStatus
from app.models.user import User
import asyncio
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from PIL import Image
import io
import base64
import re
import requests
from app.core.logger import logger

@dataclass
class CompressionResult:
    """Result of image compression operation."""
    success: bool
    data: Optional[bytes] = None
    error: Optional[str] = None
    original_size: Optional[int] = None
    compressed_size: Optional[int] = None

class VerificationService:
    @staticmethod
    async def create_verification_request(
        db: Client,
        user: User,
        request: VerificationRequestCreate
    ) -> VerificationRequestResponse:
        """Create a new verification request."""
        verification_data = {
            "user_id": user.id,
            "verification_type": request.verification_type,
            "status": VerificationRequestStatus.PENDING,
            "submitted_at": datetime.utcnow().isoformat(),
            "evidence": request.evidence,
            "notes": request.notes
        }
        
        response = await db.table("verification_requests").insert(verification_data).execute()
        return VerificationRequestResponse(**response.data[0])

    @staticmethod
    async def get_verification_request(
        db: Client,
        request_id: str
    ) -> Optional[VerificationRequestResponse]:
        """Get a verification request by ID."""
        response = await db.table("verification_requests").select("*").eq("id", request_id).execute()
        if not response.data:
            return None
        return VerificationRequestResponse(**response.data[0])

    @staticmethod
    async def get_user_verification_requests(
        db: Client,
        user_id: str,
        status: Optional[VerificationRequestStatus] = None
    ) -> List[VerificationRequestResponse]:
        """Get all verification requests for a user."""
        query = db.table("verification_requests").select("*").eq("user_id", user_id)
        if status:
            query = query.eq("status", status)
        
        response = await query.execute()
        return [VerificationRequestResponse(**item) for item in response.data]

    @staticmethod
    async def update_verification_request(
        db: Client,
        request_id: str,
        update: VerificationRequestUpdate,
        reviewer_id: str
    ) -> Optional[VerificationRequestResponse]:
        """Update a verification request."""
        update_data = update.model_dump(exclude_unset=True)
        update_data["reviewed_at"] = datetime.utcnow().isoformat()
        update_data["reviewed_by"] = reviewer_id

        response = await db.table("verification_requests").update(update_data).eq("id", request_id).execute()
        if not response.data:
            return None
        
        # Update user's profile verification status if request is approved/rejected
        if update.status in [VerificationRequestStatus.APPROVED, VerificationRequestStatus.REJECTED]:
            await VerificationService._update_profile_verification(
                db,
                response.data[0]["user_id"],
                response.data[0]["verification_type"],
                update.status
            )
        
        return VerificationRequestResponse(**response.data[0])

    @staticmethod
    async def _update_profile_verification(
        db: Client,
        user_id: str,
        verification_type: VerificationType,
        status: VerificationRequestStatus
    ) -> None:
        """Update user's profile verification status."""
        # Get current verification status
        response = await db.table("users").select("profile_verification").eq("id", user_id).execute()
        current_verification = response.data[0].get("profile_verification", {})
        
        # Update verified fields based on verification type
        verified_fields = current_verification.get("verified_fields", [])
        if status == VerificationRequestStatus.APPROVED:
            if verification_type == VerificationType.IDENTITY:
                verified_fields.extend(["first_name", "last_name", "email", "phone"])
            elif verification_type == VerificationType.EDUCATION:
                verified_fields.extend(["education"])
            elif verification_type == VerificationType.EMPLOYMENT:
                verified_fields.extend(["work_experience"])
            elif verification_type == VerificationType.SKILLS:
                verified_fields.extend(["skills"])
            elif verification_type == VerificationType.CERTIFICATIONS:
                verified_fields.extend(["certifications"])
            elif verification_type == VerificationType.PORTFOLIO:
                verified_fields.extend(["portfolio"])
        
        # Update verification status
        new_verification = {
            "status": ProfileVerificationStatus.VERIFIED if len(verified_fields) > 0 else ProfileVerificationStatus.UNVERIFIED,
            "verified_fields": list(set(verified_fields)),
            "verification_date": datetime.utcnow().isoformat(),
            "verified_by": "system"
        }
        
        await db.table("users").update({"profile_verification": new_verification}).eq("id", user_id).execute()

    @staticmethod
    async def get_verification_stats(db: Client) -> VerificationStats:
        """Get verification statistics."""
        response = await db.table("verification_requests").select("*").execute()
        requests = response.data
        
        stats = VerificationStats()
        stats.total_requests = len(requests)
        
        # Count requests by status
        for request in requests:
            status = request["status"]
            if status == VerificationRequestStatus.PENDING:
                stats.pending_requests += 1
            elif status == VerificationRequestStatus.IN_REVIEW:
                stats.in_review_requests += 1
            elif status == VerificationRequestStatus.APPROVED:
                stats.approved_requests += 1
            elif status == VerificationRequestStatus.REJECTED:
                stats.rejected_requests += 1
            
            # Count requests by type
            verification_type = request["verification_type"]
            stats.requests_by_type[verification_type] = stats.requests_by_type.get(verification_type, 0) + 1
        
        # Calculate average review time
        reviewed_requests = [r for r in requests if r.get("reviewed_at") and r.get("submitted_at")]
        if reviewed_requests:
            total_time = sum(
                (datetime.fromisoformat(r["reviewed_at"]) - datetime.fromisoformat(r["submitted_at"])).total_seconds()
                for r in reviewed_requests
            )
            stats.average_review_time = total_time / len(reviewed_requests)
        
        # Get recent activity
        recent_requests = sorted(
            requests,
            key=lambda x: x.get("reviewed_at", x.get("submitted_at", "")),
            reverse=True
        )[:10]
        
        stats.recent_activity = [
            {
                "request_id": r["id"],
                "user_id": r["user_id"],
                "type": r["verification_type"],
                "status": r["status"],
                "timestamp": r.get("reviewed_at", r.get("submitted_at")),
                "reviewer": r.get("reviewed_by")
            }
            for r in recent_requests
        ]
        
        return stats 

    @staticmethod
    async def validate_document(
        file: UploadFile,
        document_type: str
    ) -> DocumentValidation:
        """Validate a document before upload."""
        # Get file extension
        file_extension = os.path.splitext(file.filename)[1].lower()
        
        # Create validation object
        validation = DocumentValidation(
            file_size=0,  # Will be updated after reading file
            mime_type=file.content_type,
            file_extension=file_extension
        )
        
        # Read file content for size validation
        content = await file.read()
        validation.file_size = len(content)
        
        # Reset file pointer
        await file.seek(0)
        
        # Validate file
        try:
            validation.validate_file_size()
            validation.validate_mime_type()
            validation.validate_extension()
            
            # Save temporarily for content validation
            temp_path = f"/tmp/{file.filename}"
            async with aiofiles.open(temp_path, 'wb') as out_file:
                await out_file.write(content)
            
            # Validate content
            validation.validate_content(temp_path)
            os.remove(temp_path)
            
        except DocumentValidationError as e:
            validation.validation_errors.append(str(e))
            validation.is_valid = False
            return validation
        
        validation.is_valid = True
        return validation

    @staticmethod
    async def _compress_document_parallel(
        file_path: str,
        validation: DocumentValidation
    ) -> Tuple[Optional[bytes], Optional[CompressionResult]]:
        """Compress a single document in a thread pool."""
        try:
            if validation.file_size <= COMPRESSION_THRESHOLD:
                return None, None

            if validation.mime_type.startswith("image/"):
                compression_result = await validation._compress_image(file_path)
            elif validation.mime_type == "application/pdf":
                compression_result = await validation._compress_pdf(file_path)
            else:
                compression_result = await validation._compress_generic(file_path)

            if compression_result and compression_result.is_compressed:
                # Read compressed content
                async with aiofiles.open(file_path, 'rb') as f:
                    compressed_content = await f.read()
                return compressed_content, compression_result

            return None, None
        except Exception as e:
            print(f"Compression error for {file_path}: {str(e)}")
            return None, None

    @staticmethod
    async def _process_batch_compression(
        files: List[Tuple[UploadFile, str, DocumentValidation]]
    ) -> List[Tuple[UploadFile, Optional[bytes], Optional[CompressionResult]]]:
        """Process multiple document compressions in parallel."""
        tasks = []
        for file, file_path, validation in files:
            task = VerificationService._compress_document_parallel(file_path, validation)
            tasks.append(task)
        
        # Run compressions in parallel with a limit on concurrent tasks
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results and handle any exceptions
        processed_results = []
        for (file, file_path, validation), (compressed_content, compression_result) in zip(files, results):
            if isinstance(compressed_content, Exception):
                print(f"Error compressing {file.filename}: {str(compressed_content)}")
                processed_results.append((file, None, None))
            else:
                processed_results.append((file, compressed_content, compression_result))
        
        return processed_results

    @staticmethod
    async def batch_upload_documents(
        db: Client,
        files: List[UploadFile],
        document_type: str,
        user_id: str,
        request_id: str
    ) -> BatchDocumentUpload:
        """Upload multiple documents in a batch with parallel compression."""
        result = BatchDocumentUpload()
        
        # Create upload directory
        upload_dir = f"verification_documents/{request_id}"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Validate all documents first
        validation_tasks = []
        for file in files:
            validation = await VerificationService.validate_document(file, document_type)
            if not validation.is_valid:
                result.failed_count += 1
                result.errors.append({
                    "file": file.filename,
                    "errors": validation.validation_errors
                })
                continue
            
            # Generate unique filename
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            file_extension = os.path.splitext(file.filename)[1]
            unique_filename = f"{timestamp}_{file.filename}"
            file_path = os.path.join(upload_dir, unique_filename)
            
            # Save file temporarily
            async with aiofiles.open(file_path, 'wb') as out_file:
                content = await file.read()
                await out_file.write(content)
            
            validation_tasks.append((file, file_path, validation))
        
        # Process compressions in parallel
        compression_results = await VerificationService._process_batch_compression(validation_tasks)
        
        # Upload documents and create records
        for file, compressed_content, compression_result in compression_results:
            try:
                # Generate unique filename
                timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
                file_extension = os.path.splitext(file.filename)[1]
                unique_filename = f"{timestamp}_{file.filename}"
                
                if compression_result and compression_result.is_compressed:
                    base_name, ext = os.path.splitext(unique_filename)
                    unique_filename = f"{base_name}_compressed{ext}"
                
                file_path = os.path.join(upload_dir, unique_filename)
                
                # Save final content (compressed or original)
                content = compressed_content if compressed_content else await file.read()
                async with aiofiles.open(file_path, 'wb') as out_file:
                    await out_file.write(content)
                
                # Upload to storage
                file_url = await VerificationService._upload_to_storage(file_path, unique_filename)
                
                # Create document record
                document = DocumentUpload(
                    document_type=document_type,
                    file_name=file.filename,
                    file_size=len(content),
                    mime_type=file.content_type,
                    file_url=file_url,
                    uploaded_at=datetime.utcnow().isoformat(),
                    uploaded_by=user_id,
                    compression_info=compression_result.model_dump() if compression_result else None
                )
                
                # Save document record to database
                await db.table("verification_documents").insert(document.model_dump()).execute()
                
                result.documents.append(document.model_dump())
                result.success_count += 1
                result.total_size += document.file_size
                
                # Add compression info if available
                if compression_result:
                    result.compression_stats.append({
                        "file": file.filename,
                        "original_size": compression_result.original_size,
                        "compressed_size": compression_result.compressed_size,
                        "compression_ratio": compression_result.compression_ratio,
                        "compression_method": compression_result.compression_method
                    })
                
                # Clean up temporary file
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Error removing temporary file: {str(e)}")
                
            except Exception as e:
                result.failed_count += 1
                result.errors.append({
                    "file": file.filename,
                    "errors": [str(e)]
                })
        
        return result

    @staticmethod
    async def _upload_to_storage(file_path: str, filename: str) -> str:
        """Upload file to cloud storage."""
        # Implementation depends on your storage provider (S3, GCS, etc.)
        # This is a placeholder implementation
        return f"{settings.STORAGE_BASE_URL}/verification_documents/{filename}"

    @staticmethod
    async def send_verification_notification(
        notification: VerificationNotification
    ) -> None:
        """Send email notification for verification status changes."""
        subject = f"Verification Request {notification.status.value.title()}"
        
        # HTML email template
        html_content = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #f8f9fa; padding: 20px; border-radius: 5px; }}
                    .content {{ padding: 20px; }}
                    .footer {{ text-align: center; padding: 20px; color: #666; }}
                    .status {{
                        display: inline-block;
                        padding: 5px 10px;
                        border-radius: 3px;
                        font-weight: bold;
                    }}
                    .status-approved {{ background-color: #d4edda; color: #155724; }}
                    .status-rejected {{ background-color: #f8d7da; color: #721c24; }}
                    .status-pending {{ background-color: #fff3cd; color: #856404; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>Verification Request Update</h2>
                    </div>
                    <div class="content">
                        <p>Dear User,</p>
                        <p>Your verification request for <strong>{notification.verification_type.value}</strong> has been 
                        <span class="status status-{notification.status.value}">{notification.status.value.title()}</span>.</p>
                        
                        {f'<p><strong>Notes:</strong> {notification.notes}</p>' if notification.notes else ''}
                        
                        {f'<p><strong>Rejection Reason:</strong> {notification.rejection_reason}</p>' if notification.rejection_reason else ''}
                        
                        {f'<p>Reviewed by: {notification.reviewer_name}</p>' if notification.reviewer_name else ''}
                        
                        {f'<p>Please submit a new request with updated information.</p>' if notification.status == VerificationRequestStatus.REJECTED else ''}
                    </div>
                    <div class="footer">
                        <p>Best regards,<br>The Verification Team</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        await send_email(
            email_to=notification.user_email,
            subject=subject,
            content=html_content,
            is_html=True
        )

    @staticmethod
    async def get_dashboard_data(db: Client) -> VerificationDashboard:
        """Get data for the verification dashboard."""
        # Get basic stats
        stats = await VerificationService.get_verification_stats(db)
        
        # Get pending requests
        pending_response = await db.table("verification_requests").select("*").eq("status", VerificationRequestStatus.PENDING).execute()
        pending_requests = [VerificationRequestResponse(**item) for item in pending_response.data]
        
        # Get verification types data
        types_response = await db.table("verification_requests").select("verification_type, status").execute()
        verification_types = {}
        for request in types_response.data:
            v_type = request["verification_type"]
            if v_type not in verification_types:
                verification_types[v_type] = {
                    "total": 0,
                    "approved": 0,
                    "rejected": 0,
                    "pending": 0
                }
            verification_types[v_type]["total"] += 1
            verification_types[v_type][request["status"]] += 1
        
        # Get top reviewers
        reviewers_response = await db.table("verification_requests").select("reviewed_by").not_.is_("reviewed_by", "null").execute()
        reviewer_counts = {}
        for request in reviewers_response.data:
            reviewer = request["reviewed_by"]
            reviewer_counts[reviewer] = reviewer_counts.get(reviewer, 0) + 1
        
        top_reviewers = [
            {"reviewer": reviewer, "count": count}
            for reviewer, count in sorted(reviewer_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        ]
        
        # Calculate completion and rejection rates
        total_requests = stats.total_requests
        completion_rate = (stats.approved_requests / total_requests * 100) if total_requests > 0 else 0
        rejection_rate = (stats.rejected_requests / total_requests * 100) if total_requests > 0 else 0
        
        # Get monthly trends
        monthly_response = await db.table("verification_requests").select("submitted_at, status").execute()
        monthly_trends = {}
        for request in monthly_response.data:
            date = datetime.fromisoformat(request["submitted_at"]).strftime("%Y-%m")
            if date not in monthly_trends:
                monthly_trends[date] = {
                    "total": 0,
                    "approved": 0,
                    "rejected": 0,
                    "pending": 0
                }
            monthly_trends[date]["total"] += 1
            monthly_trends[date][request["status"]] += 1
        
        return VerificationDashboard(
            stats=stats,
            pending_requests=pending_requests,
            recent_activity=stats.recent_activity,
            verification_types=verification_types,
            top_reviewers=top_reviewers,
            average_response_time=stats.average_review_time or 0,
            completion_rate=completion_rate,
            rejection_rate=rejection_rate,
            monthly_trends=list(monthly_trends.values())
        ) 

    @staticmethod
    async def get_daily_verification_trends(db: Client) -> List[Dict[str, Any]]:
        """Get daily verification trends for the last 30 days."""
        thirty_days_ago = (datetime.utcnow() - timedelta(days=30)).isoformat()
        
        response = await db.table("verification_requests").select(
            "submitted_at", "status"
        ).gte("submitted_at", thirty_days_ago).execute()
        
        # Group by date and status
        trends = {}
        for request in response.data:
            date = datetime.fromisoformat(request["submitted_at"]).strftime("%Y-%m-%d")
            if date not in trends:
                trends[date] = {
                    "date": date,
                    "total": 0,
                    "approved": 0,
                    "rejected": 0,
                    "pending": 0
                }
            trends[date]["total"] += 1
            trends[date][request["status"]] += 1
        
        return list(trends.values())

    @staticmethod
    async def get_weekly_verification_trends(db: Client) -> List[Dict[str, Any]]:
        """Get weekly verification trends for the last 12 weeks."""
        twelve_weeks_ago = (datetime.utcnow() - timedelta(weeks=12)).isoformat()
        
        response = await db.table("verification_requests").select(
            "submitted_at", "status"
        ).gte("submitted_at", twelve_weeks_ago).execute()
        
        # Group by week and status
        trends = {}
        for request in response.data:
            date = datetime.fromisoformat(request["submitted_at"])
            week = date.strftime("%Y-W%W")
            if week not in trends:
                trends[week] = {
                    "week": week,
                    "total": 0,
                    "approved": 0,
                    "rejected": 0,
                    "pending": 0
                }
            trends[week]["total"] += 1
            trends[week][request["status"]] += 1
        
        return list(trends.values())

    @staticmethod
    async def get_document_type_statistics(db: Client) -> Dict[str, Any]:
        """Get statistics about document types."""
        response = await db.table("verification_documents").select(
            "document_type", "file_size"
        ).execute()
        
        stats = {
            "by_type": {},
            "total_documents": len(response.data),
            "total_size": sum(doc["file_size"] for doc in response.data)
        }
        
        for doc in response.data:
            doc_type = doc["document_type"]
            if doc_type not in stats["by_type"]:
                stats["by_type"][doc_type] = {
                    "count": 0,
                    "total_size": 0,
                    "average_size": 0
                }
            stats["by_type"][doc_type]["count"] += 1
            stats["by_type"][doc_type]["total_size"] += doc["file_size"]
        
        # Calculate averages
        for doc_type in stats["by_type"]:
            count = stats["by_type"][doc_type]["count"]
            stats["by_type"][doc_type]["average_size"] = (
                stats["by_type"][doc_type]["total_size"] / count
            )
        
        return stats

    @staticmethod
    async def get_document_size_statistics(db: Client) -> Dict[str, Any]:
        """Get statistics about document sizes."""
        response = await db.table("verification_documents").select("file_size").execute()
        
        sizes = [doc["file_size"] for doc in response.data]
        return {
            "total_documents": len(sizes),
            "total_size": sum(sizes),
            "average_size": sum(sizes) / len(sizes) if sizes else 0,
            "min_size": min(sizes) if sizes else 0,
            "max_size": max(sizes) if sizes else 0,
            "size_distribution": {
                "0-1MB": len([s for s in sizes if s <= 1024 * 1024]),
                "1-5MB": len([s for s in sizes if 1024 * 1024 < s <= 5 * 1024 * 1024]),
                "5-10MB": len([s for s in sizes if 5 * 1024 * 1024 < s <= 10 * 1024 * 1024]),
                ">10MB": len([s for s in sizes if s > 10 * 1024 * 1024])
            }
        }

    @staticmethod
    async def get_document_validation_success_rate(db: Client) -> Dict[str, Any]:
        """Get document validation success rate statistics."""
        response = await db.table("verification_documents").select(
            "document_type", "validation_status"
        ).execute()
        
        stats = {
            "total_documents": len(response.data),
            "success_rate": 0,
            "by_type": {}
        }
        
        for doc in response.data:
            doc_type = doc["document_type"]
            if doc_type not in stats["by_type"]:
                stats["by_type"][doc_type] = {
                    "total": 0,
                    "valid": 0,
                    "invalid": 0,
                    "success_rate": 0
                }
            
            stats["by_type"][doc_type]["total"] += 1
            if doc.get("validation_status") == "valid":
                stats["by_type"][doc_type]["valid"] += 1
            else:
                stats["by_type"][doc_type]["invalid"] += 1
        
        # Calculate success rates
        total_valid = sum(stats["by_type"][t]["valid"] for t in stats["by_type"])
        stats["success_rate"] = (total_valid / stats["total_documents"] * 100) if stats["total_documents"] > 0 else 0
        
        for doc_type in stats["by_type"]:
            total = stats["by_type"][doc_type]["total"]
            stats["by_type"][doc_type]["success_rate"] = (
                stats["by_type"][doc_type]["valid"] / total * 100
            ) if total > 0 else 0
        
        return stats

    @staticmethod
    async def get_reviewer_activity(db: Client) -> List[Dict[str, Any]]:
        """Get reviewer activity statistics."""
        response = await db.table("verification_requests").select(
            "reviewed_by", "submitted_at", "reviewed_at", "status"
        ).not_.is_("reviewed_by", "null").execute()
        
        # Group by reviewer
        activity = {}
        for request in response.data:
            reviewer = request["reviewed_by"]
            if reviewer not in activity:
                activity[reviewer] = {
                    "reviewer": reviewer,
                    "total_reviews": 0,
                    "approved": 0,
                    "rejected": 0,
                    "average_response_time": 0,
                    "last_review": None
                }
            
            activity[reviewer]["total_reviews"] += 1
            activity[reviewer][request["status"]] += 1
            
            # Calculate response time
            submitted = datetime.fromisoformat(request["submitted_at"])
            reviewed = datetime.fromisoformat(request["reviewed_at"])
            response_time = (reviewed - submitted).total_seconds()
            
            # Update last review
            if not activity[reviewer]["last_review"] or reviewed > datetime.fromisoformat(activity[reviewer]["last_review"]):
                activity[reviewer]["last_review"] = request["reviewed_at"]
        
        # Calculate averages
        for reviewer in activity:
            total_time = sum(
                (datetime.fromisoformat(r["reviewed_at"]) - datetime.fromisoformat(r["submitted_at"])).total_seconds()
                for r in response.data
                if r["reviewed_by"] == reviewer
            )
            activity[reviewer]["average_response_time"] = (
                total_time / activity[reviewer]["total_reviews"]
            ) if activity[reviewer]["total_reviews"] > 0 else 0
        
        return list(activity.values())

    @staticmethod
    async def get_average_verification_time(db: Client) -> float:
        """Get average verification time in seconds."""
        response = await db.table("verification_requests").select(
            "submitted_at", "reviewed_at"
        ).not_.is_("reviewed_at", "null").execute()
        
        if not response.data:
            return 0
        
        total_time = sum(
            (datetime.fromisoformat(r["reviewed_at"]) - datetime.fromisoformat(r["submitted_at"])).total_seconds()
            for r in response.data
        )
        
        return total_time / len(response.data)

    @staticmethod
    async def get_verification_success_rate(db: Client) -> float:
        """Get verification success rate."""
        response = await db.table("verification_requests").select("status").execute()
        
        if not response.data:
            return 0
        
        approved = sum(1 for r in response.data if r["status"] == VerificationRequestStatus.APPROVED)
        return (approved / len(response.data)) * 100 

    @staticmethod
    def compress_image(
        image_data: bytes,
        max_size: int = 1024,
        quality: int = 85
    ) -> Tuple[Optional[bytes], Optional[CompressionResult]]:
        """
        Compress an image while maintaining aspect ratio.
        
        Args:
            image_data: Raw image data
            max_size: Maximum dimension (width or height)
            quality: JPEG quality (1-100)
            
        Returns:
            Tuple of (compressed image data, compression result)
        """
        try:
            # Open image from bytes
            img = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Calculate new dimensions maintaining aspect ratio
            ratio = max_size / max(img.size)
            new_size = tuple(int(dim * ratio) for dim in img.size)
            
            # Resize image
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Save to bytes with compression
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=quality, optimize=True)
            compressed_data = output.getvalue()
            
            # Calculate compression stats
            original_size = len(image_data)
            compressed_size = len(compressed_data)
            
            result = CompressionResult(
                success=True,
                data=compressed_data,
                original_size=original_size,
                compressed_size=compressed_size
            )
            
            return compressed_data, result
            
        except Exception as e:
            logger.error(f"Error compressing image: {str(e)}")
            result = CompressionResult(
                success=False,
                error=str(e)
            )
            return None, result 