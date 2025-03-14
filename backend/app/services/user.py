from typing import Optional, List, Dict, Any
from datetime import datetime
from supabase import Client
from fastapi import UploadFile
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.profile import ProfilePictureCompression
from app.core.config import settings
import os
import shutil

class UserService:
    @staticmethod
    async def update_profile_picture(
        db: Client,
        user_id: str,
        file: UploadFile
    ) -> Optional[Dict[str, Any]]:
        """Update user's profile picture with compression."""
        try:
            # Compress profile picture
            compression_result = await ProfilePictureCompression.compress_profile_picture(file, user_id)
            if not compression_result["success"]:
                return {
                    "success": False,
                    "error": compression_result["error"]
                }
            
            # Generate thumbnail
            thumbnail_result = await ProfilePictureCompression.generate_thumbnail(
                compression_result["temp_path"]
            )
            
            if not thumbnail_result["success"]:
                # Clean up temp files
                await ProfilePictureCompression.cleanup_temp_files([compression_result["temp_path"]])
                return {
                    "success": False,
                    "error": thumbnail_result["error"]
                }
            
            # Move files to permanent storage
            profile_path = os.path.join(
                settings.UPLOAD_DIR,
                settings.PROFILE_PICTURES_DIR,
                compression_result["filename"]
            )
            
            thumbnail_path = os.path.join(
                settings.UPLOAD_DIR,
                settings.PROFILE_PICTURES_DIR,
                f"thumb_{compression_result['filename']}"
            )
            
            # Move files from temp to permanent storage
            shutil.move(compression_result["temp_path"], profile_path)
            shutil.move(thumbnail_result["thumbnail_path"], thumbnail_path)
            
            # Get relative paths for URLs
            profile_url = settings.get_file_url(
                os.path.join(settings.PROFILE_PICTURES_DIR, compression_result["filename"])
            )
            
            thumbnail_url = settings.get_file_url(
                os.path.join(settings.PROFILE_PICTURES_DIR, f"thumb_{compression_result['filename']}")
            )
            
            # Update user record
            update_data = {
                "profile_picture": profile_url,
                "profile_picture_thumb": thumbnail_url,
                "profile_picture_updated_at": datetime.utcnow().isoformat(),
                "profile_picture_metadata": {
                    "original_size": compression_result["original_size"],
                    "compressed_size": compression_result["compressed_size"],
                    "compression_ratio": compression_result["compression_ratio"],
                    "dimensions": compression_result["dimensions"],
                    "format": compression_result["format"],
                    "thumbnail_dimensions": thumbnail_result["dimensions"],
                    "local_path": profile_path,
                    "local_thumb_path": thumbnail_path
                }
            }
            
            response = await db.table("users").update(update_data).eq("id", user_id).execute()
            
            return {
                "success": True,
                "profile_picture": profile_url,
                "profile_picture_thumb": thumbnail_url,
                "metadata": update_data["profile_picture_metadata"]
            }
            
        except Exception as e:
            # Clean up any temporary files
            temp_files = [
                compression_result.get("temp_path"),
                thumbnail_result.get("thumbnail_path")
            ]
            await ProfilePictureCompression.cleanup_temp_files([f for f in temp_files if f])
            
            return {
                "success": False,
                "error": str(e)
            }

    @staticmethod
    async def delete_profile_picture(
        db: Client,
        user_id: str
    ) -> bool:
        """Delete user's profile picture and thumbnail."""
        try:
            # Get user's profile picture metadata
            response = await db.table("users").select("profile_picture_metadata").eq("id", user_id).execute()
            if not response.data or not response.data[0].get("profile_picture_metadata"):
                return False
            
            metadata = response.data[0]["profile_picture_metadata"]
            
            # Delete files
            for file_path in [metadata.get("local_path"), metadata.get("local_thumb_path")]:
                if file_path and os.path.exists(file_path):
                    os.remove(file_path)
            
            # Update user record
            await db.table("users").update({
                "profile_picture": None,
                "profile_picture_thumb": None,
                "profile_picture_metadata": None
            }).eq("id", user_id).execute()
            
            return True
            
        except Exception as e:
            print(f"Error deleting profile picture: {str(e)}")
            return False

    @staticmethod
    async def _upload_to_storage(file_path: str, filename: str) -> str:
        """Upload file to cloud storage."""
        # Implementation depends on your storage provider (S3, GCS, etc.)
        # This is a placeholder implementation
        return f"{settings.STORAGE_BASE_URL}/profile_pictures/{filename}" 