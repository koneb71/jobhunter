import io
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import aiofiles
from fastapi import UploadFile
from PIL import Image

from app.core.config import settings
from app.schemas.profile import (
    ProfileAnalytics,
    ProfileScore,
    ProfileStrength,
    ProfileVerification,
    ProfileVerificationStatus,
    SkillEndorsement,
    SkillLevel,
    SkillRating,
)
from app.schemas.user import ProfilePictureMetadata, UserResponse


class ProfileService:
    @staticmethod
    def calculate_profile_score(user: UserResponse) -> ProfileScore:
        """Calculate profile completion score and strength."""
        total_fields = 0
        completed_fields = 0
        missing_fields = []
        recommendations = []

        # Basic Information
        total_fields += 4
        if user.full_name:
            completed_fields += 1
        else:
            missing_fields.append("full_name")
            recommendations.append("Add your full name")

        if user.email:
            completed_fields += 1
        else:
            missing_fields.append("email")
            recommendations.append("Add your email address")

        if user.phone:
            completed_fields += 1
        else:
            missing_fields.append("phone")
            recommendations.append("Add your phone number")

        if user.bio:
            completed_fields += 1
        else:
            missing_fields.append("bio")
            recommendations.append("Add your bio")

        # Professional Information
        total_fields += 3
        if user.tagline:
            completed_fields += 1
        else:
            missing_fields.append("tagline")
            recommendations.append("Add a professional tagline")

        if user.profile_overview:
            completed_fields += 1
        else:
            missing_fields.append("profile_overview")
            recommendations.append("Add a profile overview")

        if user.location:
            completed_fields += 1
        else:
            missing_fields.append("location")
            recommendations.append("Add your location")

        # Skills and Experience
        total_fields += 2
        if user.skills:
            completed_fields += 1
        else:
            missing_fields.append("skills")
            recommendations.append("Add your skills")

        if user.work_experience:
            completed_fields += 1
        else:
            missing_fields.append("work_experience")
            recommendations.append("Add your work experience")

        # Education
        total_fields += 1
        if user.education:
            completed_fields += 1
        else:
            missing_fields.append("education")
            recommendations.append("Add your education history")

        # Portfolio
        total_fields += 1
        if user.portfolio:
            completed_fields += 1
        else:
            missing_fields.append("portfolio")
            recommendations.append("Add your portfolio projects")

        # Calculate completion percentage
        completion_percentage = (completed_fields / total_fields) * 100

        # Determine profile strength
        if completion_percentage < 30:
            strength = ProfileStrength.BEGINNER
        elif completion_percentage < 60:
            strength = ProfileStrength.INTERMEDIATE
        elif completion_percentage < 90:
            strength = ProfileStrength.ADVANCED
        else:
            strength = ProfileStrength.EXPERT

        return ProfileScore(
            completion_percentage=completion_percentage,
            strength=strength,
            missing_fields=missing_fields,
            recommendations=recommendations,
            last_updated=datetime.utcnow().isoformat(),
        )

    @staticmethod
    def calculate_skill_rating(
        skill: str, work_experience: List[Dict[str, Any]]
    ) -> SkillRating:
        """Calculate skill rating based on work experience."""
        total_years = 0
        last_used = None

        for exp in work_experience:
            if skill in exp.get("skills_used", []):
                start_date = datetime.fromisoformat(exp["start_date"])
                end_date = (
                    datetime.fromisoformat(exp["end_date"])
                    if exp.get("end_date")
                    else datetime.utcnow()
                )
                years = (end_date - start_date).days / 365.25
                total_years += years

                if not last_used or end_date > last_used:
                    last_used = end_date

        # Determine skill level based on years of experience
        if total_years < 1:
            level = SkillLevel.BEGINNER
        elif total_years < 3:
            level = SkillLevel.INTERMEDIATE
        elif total_years < 5:
            level = SkillLevel.ADVANCED
        else:
            level = SkillLevel.EXPERT

        return SkillRating(
            skill=skill,
            level=level,
            years_of_experience=round(total_years, 1),
            last_used=last_used.isoformat() if last_used else None,
        )

    @staticmethod
    def create_skill_endorsement(
        skill: str, endorser_id: str, endorser_name: str, comment: Optional[str] = None
    ) -> SkillEndorsement:
        """Create a new skill endorsement."""
        return SkillEndorsement(
            skill=skill,
            endorser_id=endorser_id,
            endorser_name=endorser_name,
            endorsement_date=datetime.utcnow().isoformat(),
            comment=comment,
        )

    @staticmethod
    def update_profile_verification(
        current_verification: Optional[ProfileVerification],
        field: str,
        verified_by: str,
        notes: Optional[str] = None,
    ) -> ProfileVerification:
        """Update profile verification status."""
        if not current_verification:
            current_verification = ProfileVerification()

        verified_fields = current_verification.verified_fields.copy()
        if field not in verified_fields:
            verified_fields.append(field)

        return ProfileVerification(
            status=(
                ProfileVerificationStatus.VERIFIED
                if len(verified_fields) > 0
                else ProfileVerificationStatus.UNVERIFIED
            ),
            verified_fields=verified_fields,
            verification_date=datetime.utcnow().isoformat(),
            verified_by=verified_by,
            notes=notes,
        )

    @staticmethod
    def update_profile_analytics(
        current_analytics: Optional[ProfileAnalytics],
        view_type: str = "view",
        skill_trend: Optional[Dict[str, Any]] = None,
        preference_change: Optional[Dict[str, Any]] = None,
    ) -> ProfileAnalytics:
        """Update profile analytics."""
        if not current_analytics:
            current_analytics = ProfileAnalytics()

        analytics = current_analytics.dict()

        if view_type == "view":
            analytics["views"] += 1
            analytics["unique_views"] += 1
            analytics["last_viewed"] = datetime.utcnow().isoformat()
        elif view_type == "search":
            analytics["search_appearances"] += 1

        if skill_trend:
            analytics["skill_trends"].append(
                {**skill_trend, "timestamp": datetime.utcnow().isoformat()}
            )

        if preference_change:
            analytics["preference_changes"].append(
                {**preference_change, "timestamp": datetime.utcnow().isoformat()}
            )

        return ProfileAnalytics(**analytics)

    @staticmethod
    def get_profile_completion(user: UserResponse) -> Dict[str, Any]:
        """Calculate profile completion percentage and missing fields."""
        required_fields = ["full_name", "email", "phone", "bio", "location"]
        missing_fields = []

        # Check basic user fields
        if not user.full_name:
            missing_fields.append("full_name")
        if not user.email:
            missing_fields.append("email")

        # Check profile fields
        if user.profile:
            if not user.profile.phone:
                missing_fields.append("phone")
            if not user.profile.bio:
                missing_fields.append("bio")
            if not user.profile.location:
                missing_fields.append("location")
        else:
            missing_fields.extend(["phone", "bio", "location"])

        # Calculate completion percentage
        completed_fields = len(required_fields) - len(missing_fields)
        completion_percentage = (completed_fields / len(required_fields)) * 100

        return {
            "completion_percentage": completion_percentage,
            "missing_fields": missing_fields,
            "required_fields": required_fields,
        }


# Profile picture settings
PROFILE_PICTURE_SETTINGS = {
    "max_size": 5 * 1024 * 1024,  # 5MB
    "max_dimensions": (800, 800),  # Max width/height
    "quality": 85,  # JPEG quality (0-100)
    "allowed_formats": ["image/jpeg", "image/png"],
    "allowed_extensions": [".jpg", ".jpeg", ".png"],
    "thumbnail_sizes": {"small": (100, 100), "medium": (200, 200), "large": (400, 400)},
}


class ProfilePictureCompression:
    @staticmethod
    async def compress_profile_picture(
        file: UploadFile, user_id: str
    ) -> Dict[str, Any]:
        """Compress and optimize a profile picture."""
        try:
            # Validate file type
            if file.content_type not in PROFILE_PICTURE_SETTINGS["allowed_formats"]:
                raise ValueError(
                    f"Unsupported file type. Allowed types: {', '.join(PROFILE_PICTURE_SETTINGS['allowed_formats'])}"
                )

            # Read file content
            content = await file.read()
            if len(content) > PROFILE_PICTURE_SETTINGS["max_size"]:
                raise ValueError(
                    f"File too large. Maximum size: {PROFILE_PICTURE_SETTINGS['max_size']/1024/1024}MB"
                )

            # Open image with PIL
            image = Image.open(io.BytesIO(content))

            # Convert to RGB if necessary
            if image.mode in ("RGBA", "LA"):
                background = Image.new("RGB", image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[-1])
                image = background

            # Resize if needed
            if (
                image.size[0] > PROFILE_PICTURE_SETTINGS["max_dimensions"][0]
                or image.size[1] > PROFILE_PICTURE_SETTINGS["max_dimensions"][1]
            ):
                image.thumbnail(
                    PROFILE_PICTURE_SETTINGS["max_dimensions"], Image.Resampling.LANCZOS
                )

            # Save compressed image
            output = io.BytesIO()
            image.save(
                output,
                format="JPEG",
                quality=PROFILE_PICTURE_SETTINGS["quality"],
                optimize=True,
            )
            compressed_content = output.getvalue()

            # Calculate compression stats
            original_size = len(content)
            compressed_size = len(compressed_content)
            compression_ratio = compressed_size / original_size

            # Generate unique filename
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            file_extension = os.path.splitext(file.filename)[1].lower()
            unique_filename = f"profile_{user_id}_{timestamp}{file_extension}"

            # Save to temporary file
            temp_path = os.path.join(
                settings.UPLOAD_DIR, settings.TEMP_DIR, unique_filename
            )
            os.makedirs(os.path.dirname(temp_path), exist_ok=True)

            async with aiofiles.open(temp_path, "wb") as out_file:
                await out_file.write(compressed_content)

            return {
                "success": True,
                "filename": unique_filename,
                "temp_path": temp_path,
                "metadata": ProfilePictureMetadata(
                    original_size=original_size,
                    compressed_size=compressed_size,
                    compression_ratio=compression_ratio,
                    dimensions=image.size,
                    format=image.format,
                    thumbnail_dimensions={},  # Will be populated by generate_thumbnails
                    local_path=temp_path,
                    created_at=datetime.utcnow().isoformat(),
                ),
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    async def generate_thumbnails(image_path: str, user_id: str) -> Dict[str, Any]:
        """Generate multiple thumbnail versions of the profile picture."""
        try:
            thumbnails = {}
            # Open the original image
            with Image.open(image_path) as image:
                # Convert to RGB if necessary
                if image.mode in ("RGBA", "LA"):
                    background = Image.new("RGB", image.size, (255, 255, 255))
                    background.paste(image, mask=image.split()[-1])
                    image = background

                # Generate thumbnails for each size
                for size_name, size in PROFILE_PICTURE_SETTINGS[
                    "thumbnail_sizes"
                ].items():
                    # Create a copy of the image for this thumbnail
                    thumb = image.copy()
                    # Create thumbnail
                    thumb.thumbnail(size, Image.Resampling.LANCZOS)

                    # Generate thumbnail filename
                    base_name, ext = os.path.splitext(image_path)
                    thumb_filename = (
                        f"thumb_{size_name}_{os.path.basename(base_name)}{ext}"
                    )
                    thumb_path = os.path.join(
                        settings.UPLOAD_DIR, settings.TEMP_DIR, thumb_filename
                    )

                    # Save thumbnail
                    thumb.save(
                        thumb_path,
                        format="JPEG",
                        quality=PROFILE_PICTURE_SETTINGS["quality"],
                        optimize=True,
                    )

                    thumbnails[size_name] = {
                        "path": thumb_path,
                        "filename": thumb_filename,
                        "dimensions": thumb.size,
                    }

                return {"success": True, "thumbnails": thumbnails}

        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    async def cleanup_temp_files(file_paths: List[str]) -> None:
        """Clean up temporary files."""
        for path in file_paths:
            try:
                if os.path.exists(path):
                    os.remove(path)
            except Exception as e:
                print(f"Error removing temporary file {path}: {str(e)}")
