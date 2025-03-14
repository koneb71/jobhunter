import React from 'react';
import { motion } from 'framer-motion';
import ProfilePictureManager from '../components/profile/ProfilePictureManager';
import { useProfilePicture } from '../hooks/useProfilePicture';
import { useAuth } from '../hooks/useAuth';

const UserProfile: React.FC = () => {
  const { user } = useAuth();
  const { uploadProfilePicture, deleteProfilePicture, isUploading } = useProfilePicture({
    userId: user?.id || '',
    onSuccess: () => {
      // Refresh user data or update local state
    },
  });

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="bg-white rounded-2xl shadow-sm p-8"
        >
          <div className="flex flex-col items-center space-y-6">
            <ProfilePictureManager
              picture={user.profile_picture}
              thumbnail={user.profile_picture_thumb}
              onUpload={uploadProfilePicture}
              onDelete={deleteProfilePicture}
              className="mb-4"
            />

            <div className="text-center">
              <h1 className="text-2xl font-bold text-gray-900">{user.name}</h1>
              <p className="text-gray-600">{user.email}</p>
            </div>

            {user.profile_picture_metadata && (
              <div className="w-full max-w-md bg-gray-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-gray-900 mb-2">Image Details</h3>
                <div className="grid grid-cols-2 gap-4 text-sm text-gray-600">
                  <div>
                    <span className="font-medium">Original Size:</span>
                    <span className="ml-2">
                      {(user.profile_picture_metadata.original_size / 1024).toFixed(2)} KB
                    </span>
                  </div>
                  <div>
                    <span className="font-medium">Compressed Size:</span>
                    <span className="ml-2">
                      {(user.profile_picture_metadata.compressed_size / 1024).toFixed(2)} KB
                    </span>
                  </div>
                  <div>
                    <span className="font-medium">Compression Ratio:</span>
                    <span className="ml-2">
                      {(user.profile_picture_metadata.compression_ratio * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div>
                    <span className="font-medium">Dimensions:</span>
                    <span className="ml-2">
                      {user.profile_picture_metadata.dimensions[0]} x{' '}
                      {user.profile_picture_metadata.dimensions[1]}
                    </span>
                  </div>
                  <div>
                    <span className="font-medium">Format:</span>
                    <span className="ml-2">{user.profile_picture_metadata.format}</span>
                  </div>
                  <div>
                    <span className="font-medium">Last Updated:</span>
                    <span className="ml-2">
                      {new Date(user.profile_picture_updated_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default UserProfile; 