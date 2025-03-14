import { useState } from 'react';
import { toast } from 'react-hot-toast';
import { api } from '../lib/api';

interface UseProfilePictureProps {
  userId: string;
  onSuccess?: () => void;
}

interface ProfilePictureResponse {
  profile_picture: string;
  profile_picture_thumb: string;
  profile_picture_updated_at: string;
  profile_picture_metadata: {
    original_size: number;
    compressed_size: number;
    compression_ratio: number;
    dimensions: [number, number];
    format: string;
    thumbnail_dimensions: Record<string, [number, number]>;
  };
}

export const useProfilePicture = ({ userId, onSuccess }: UseProfilePictureProps) => {
  const [isUploading, setIsUploading] = useState(false);

  const uploadProfilePicture = async (file: File) => {
    try {
      setIsUploading(true);

      // Validate file size (5MB limit)
      if (file.size > 5 * 1024 * 1024) {
        throw new Error('File size must be less than 5MB');
      }

      // Validate file type
      const validTypes = ['image/jpeg', 'image/png'];
      if (!validTypes.includes(file.type)) {
        throw new Error('File must be a JPEG or PNG image');
      }

      const formData = new FormData();
      formData.append('file', file);

      const response = await api.post<ProfilePictureResponse>(
        `/users/${userId}/profile-picture`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      toast.success('Profile picture updated successfully');
      onSuccess?.();

      return response.data;
    } catch (error) {
      console.error('Failed to upload profile picture:', error);
      toast.error(error instanceof Error ? error.message : 'Failed to upload profile picture');
      throw error;
    } finally {
      setIsUploading(false);
    }
  };

  const deleteProfilePicture = async () => {
    try {
      setIsUploading(true);
      await api.delete(`/users/${userId}/profile-picture`);
      toast.success('Profile picture deleted successfully');
      onSuccess?.();
    } catch (error) {
      console.error('Failed to delete profile picture:', error);
      toast.error('Failed to delete profile picture');
      throw error;
    } finally {
      setIsUploading(false);
    }
  };

  return {
    uploadProfilePicture,
    deleteProfilePicture,
    isUploading,
  };
}; 