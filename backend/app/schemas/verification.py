import io
import os
import zipfile
from enum import Enum
from typing import Any, Dict, List, Optional

import magic
from PIL import Image
from pydantic import BaseModel, EmailStr, Field, validator

# Document validation constants
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
COMPRESSION_THRESHOLD = 5 * 1024 * 1024  # 5MB
ALLOWED_MIME_TYPES = {
    "application/pdf": [".pdf"],
    "image/jpeg": [".jpg", ".jpeg"],
    "image/png": [".png"],
    "application/msword": [".doc"],
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [
        ".docx"
    ],
    "application/vnd.ms-excel": [".xls"],
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"],
    "text/plain": [".txt"],
}

# Compression settings
COMPRESSION_QUALITY = {
    "image/jpeg": 85,  # JPEG quality (0-100)
    "image/png": 85,  # PNG quality (0-100)
    "application/pdf": 60,  # PDF compression level (0-100)
}


class DocumentValidationError(Exception):
    pass


class CompressionResult(BaseModel):
    original_size: int
    compressed_size: int
    compression_ratio: float
    compression_method: str
    is_compressed: bool = False


class DocumentValidation(BaseModel):
    file_size: int
    mime_type: str
    file_extension: str
    content_type: Optional[str] = None
    is_valid: bool = False
    validation_errors: List[str] = Field(default_factory=list)
    compression_result: Optional[CompressionResult] = None

    @validator("file_size")
    def validate_file_size(cls, v):
        if v > MAX_FILE_SIZE:
            raise DocumentValidationError(
                f"File size exceeds maximum limit of {MAX_FILE_SIZE/1024/1024}MB"
            )
        return v

    @validator("mime_type")
    def validate_mime_type(cls, v):
        if v not in ALLOWED_MIME_TYPES:
            raise DocumentValidationError(f"Unsupported file type: {v}")
        return v

    @validator("file_extension")
    def validate_extension(cls, v, values):
        if "mime_type" in values and v.lower() not in ALLOWED_MIME_TYPES.get(
            values["mime_type"], []
        ):
            raise DocumentValidationError(
                f"File extension {v} does not match mime type {values['mime_type']}"
            )
        return v.lower()

    def validate_content(self, file_path: str) -> bool:
        try:
            # Use python-magic to detect file type from content
            mime = magic.Magic(mime=True)
            content_type = mime.from_file(file_path)

            # Validate content type matches mime type
            if content_type != self.mime_type:
                self.validation_errors.append(
                    f"Content type mismatch: detected {content_type}, expected {self.mime_type}"
                )
                return False

            self.content_type = content_type
            self.is_valid = True
            return True
        except Exception as e:
            self.validation_errors.append(f"Content validation error: {str(e)}")
            return False

    async def compress_document(self, file_path: str) -> Optional[CompressionResult]:
        """Compress document if it exceeds the threshold."""
        if self.file_size <= COMPRESSION_THRESHOLD:
            return None

        try:
            if self.mime_type.startswith("image/"):
                return await self._compress_image(file_path)
            elif self.mime_type == "application/pdf":
                return await self._compress_pdf(file_path)
            else:
                return await self._compress_generic(file_path)
        except Exception as e:
            self.validation_errors.append(f"Compression error: {str(e)}")
            return None

    async def _compress_image(self, file_path: str) -> CompressionResult:
        """Compress image files."""
        quality = COMPRESSION_QUALITY.get(self.mime_type, 85)

        # Open and compress image
        with Image.open(file_path) as img:
            # Convert to RGB if necessary
            if img.mode in ("RGBA", "LA"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background

            # Save compressed image
            output = io.BytesIO()
            img.save(
                output, format=img.format or "JPEG", quality=quality, optimize=True
            )
            compressed_size = output.tell()

            return CompressionResult(
                original_size=self.file_size,
                compressed_size=compressed_size,
                compression_ratio=compressed_size / self.file_size,
                compression_method=f"image_compression_{quality}",
                is_compressed=True,
            )

    async def _compress_pdf(self, file_path: str) -> CompressionResult:
        """Compress PDF files."""
        COMPRESSION_QUALITY.get(self.mime_type, 60)

        # Use PyPDF2 or similar library for PDF compression
        # This is a placeholder implementation
        return CompressionResult(
            original_size=self.file_size,
            compressed_size=self.file_size,  # Implement actual PDF compression
            compression_ratio=1.0,
            compression_method="pdf_compression",
            is_compressed=False,
        )

    async def _compress_generic(self, file_path: str) -> CompressionResult:
        """Compress other file types using ZIP."""
        output = io.BytesIO()
        with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(file_path, os.path.basename(file_path))
        compressed_size = output.tell()

        return CompressionResult(
            original_size=self.file_size,
            compressed_size=compressed_size,
            compression_ratio=compressed_size / self.file_size,
            compression_method="zip_compression",
            is_compressed=True,
        )


class VerificationRequestStatus(str, Enum):
    PENDING = "pending"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class VerificationType(str, Enum):
    IDENTITY = "identity"
    EDUCATION = "education"
    EMPLOYMENT = "employment"
    SKILLS = "skills"
    CERTIFICATIONS = "certifications"
    PORTFOLIO = "portfolio"


class VerificationRequest(BaseModel):
    id: Optional[str] = None
    user_id: str
    verification_type: VerificationType
    status: VerificationRequestStatus = VerificationRequestStatus.PENDING
    submitted_at: Optional[str] = None
    reviewed_at: Optional[str] = None
    reviewed_by: Optional[str] = None
    notes: Optional[str] = None
    evidence: Dict[str, Any] = Field(default_factory=dict)
    rejection_reason: Optional[str] = None


class DocumentType(str, Enum):
    ID_PROOF = "id_proof"
    EDUCATIONAL_CERTIFICATE = "educational_certificate"
    EMPLOYMENT_LETTER = "employment_letter"
    SKILL_CERTIFICATE = "skill_certificate"
    PORTFOLIO_PROJECT = "portfolio_project"
    OTHER = "other"


class DocumentUpload(BaseModel):
    document_type: DocumentType
    file_name: str
    file_size: int
    mime_type: str
    file_url: str
    uploaded_at: str
    uploaded_by: str


class VerificationEvidence(BaseModel):
    documents: List[DocumentUpload] = Field(default_factory=list)
    links: List[str] = Field(default_factory=list)
    additional_info: Dict[str, Any] = Field(default_factory=dict)


class VerificationRequestCreate(BaseModel):
    verification_type: VerificationType
    evidence: VerificationEvidence = Field(default_factory=dict)
    notes: Optional[str] = None


class VerificationRequestUpdate(BaseModel):
    status: Optional[VerificationRequestStatus] = None
    notes: Optional[str] = None
    evidence: Optional[Dict[str, Any]] = None
    rejection_reason: Optional[str] = None


class VerificationRequestResponse(BaseModel):
    id: str
    user_id: str
    verification_type: VerificationType
    status: VerificationRequestStatus
    submitted_at: str
    reviewed_at: Optional[str] = None
    reviewed_by: Optional[str] = None
    notes: Optional[str] = None
    evidence: Dict[str, Any]
    rejection_reason: Optional[str] = None


class VerificationStats(BaseModel):
    total_requests: int = 0
    pending_requests: int = 0
    approved_requests: int = 0
    rejected_requests: int = 0
    in_review_requests: int = 0
    requests_by_type: Dict[str, int] = Field(default_factory=dict)
    average_review_time: Optional[float] = None
    recent_activity: List[Dict[str, Any]] = Field(default_factory=list)


class VerificationNotification(BaseModel):
    user_email: EmailStr
    request_id: str
    verification_type: VerificationType
    status: VerificationRequestStatus
    notes: Optional[str] = None
    rejection_reason: Optional[str] = None
    reviewer_name: Optional[str] = None


class VerificationDashboard(BaseModel):
    stats: VerificationStats
    pending_requests: List[VerificationRequestResponse]
    recent_activity: List[Dict[str, Any]]
    verification_types: Dict[str, Dict[str, Any]]
    top_reviewers: List[Dict[str, Any]]
    average_response_time: float
    completion_rate: float
    rejection_rate: float
    monthly_trends: List[Dict[str, Any]]


class BatchDocumentUpload(BaseModel):
    documents: List[Dict[str, Any]] = Field(default_factory=list)
    total_size: int = 0
    success_count: int = 0
    failed_count: int = 0
    errors: List[Dict[str, Any]] = Field(default_factory=list)
