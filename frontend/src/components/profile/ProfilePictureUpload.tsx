import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, X } from 'lucide-react';
import { toast } from 'react-hot-toast';

interface ProfilePictureUploadProps {
  currentPicture?: string;
  currentThumbnail?: string;
  onUpload: (url: string, thumbnail: string) => void;
}

const ProfilePictureUpload: React.FC<ProfilePictureUploadProps> = ({
  currentPicture,
  currentThumbnail,
  onUpload,
}) => {
  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;

    // Check file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      toast.error('File size must be less than 5MB');
      return;
    }

    // Check file type
    if (!file.type.startsWith('image/')) {
      toast.error('File must be an image');
      return;
    }

    try {
      const formData = new FormData();
      formData.append('file', file);

      // TODO: Replace with actual API call
      const response = await fetch('/api/upload/profile-picture', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Failed to upload image');

      const data = await response.json();
      onUpload(data.url, data.thumbnail);
      toast.success('Profile picture updated successfully');
    } catch (error) {
      toast.error('Failed to upload profile picture');
      console.error('Error uploading profile picture:', error);
    }
  }, [onUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.gif'],
    },
    maxFiles: 1,
  });

  return (
    <div className="relative">
      <div
        {...getRootProps()}
        className={`relative h-32 w-32 mx-auto rounded-full overflow-hidden border-2 border-dashed cursor-pointer transition-colors ${
          isDragActive
            ? 'border-blue-500 bg-blue-50'
            : 'border-gray-300 hover:border-gray-400'
        }`}
      >
        <input {...getInputProps()} />
        {currentPicture ? (
          <img
            src={currentPicture}
            alt="Profile"
            className="h-full w-full object-cover"
          />
        ) : (
          <div className="h-full w-full flex items-center justify-center">
            <Upload className="h-8 w-8 text-gray-400" />
          </div>
        )}
        <div className="absolute inset-0 bg-black bg-opacity-0 hover:bg-opacity-40 transition-opacity flex items-center justify-center">
          <span className="text-white text-sm font-medium opacity-0 hover:opacity-100 transition-opacity">
            Change Photo
          </span>
        </div>
      </div>
      {currentPicture && (
        <button
          onClick={(e) => {
            e.stopPropagation();
            onUpload('', '');
          }}
          className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600 transition-colors"
        >
          <X className="h-4 w-4" />
        </button>
      )}
    </div>
  );
};

export default ProfilePictureUpload; 