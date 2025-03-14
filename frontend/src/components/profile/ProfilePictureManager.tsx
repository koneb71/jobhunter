import React, { useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiCamera, FiX, FiTrash2, FiMaximize } from 'react-icons/fi';
import ProfilePictureUpload from './ProfilePictureUpload';
import ProfilePictureDisplay from './ProfilePictureDisplay';

interface ProfilePictureManagerProps {
  picture?: string;
  thumbnail?: string;
  onUpload: (file: File) => Promise<void>;
  onDelete?: () => Promise<void>;
  className?: string;
}

const ProfilePictureManager: React.FC<ProfilePictureManagerProps> = ({
  picture,
  thumbnail,
  onUpload,
  onDelete,
  className = '',
}) => {
  const [isUploading, setIsUploading] = useState(false);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [showFullscreen, setShowFullscreen] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  const handleUpload = async (file: File) => {
    try {
      setIsUploading(true);
      await onUpload(file);
      setShowUploadModal(false);
    } catch (error) {
      console.error('Failed to upload profile picture:', error);
    } finally {
      setIsUploading(false);
    }
  };

  const handleDelete = useCallback(async () => {
    if (!onDelete) return;
    
    try {
      setIsDeleting(true);
      await onDelete();
      setShowFullscreen(false);
    } catch (error) {
      console.error('Failed to delete profile picture:', error);
    } finally {
      setIsDeleting(false);
    }
  }, [onDelete]);

  return (
    <div className={`relative ${className}`}>
      <div className="relative group">
        <ProfilePictureDisplay
          picture={picture}
          thumbnail={thumbnail}
          size="large"
          className="transition-transform duration-200 group-hover:scale-105 cursor-pointer"
          onClick={() => picture && setShowFullscreen(true)}
        />
        
        <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-40 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-200">
          <div className="flex space-x-2">
            <motion.button
              className="p-2 rounded-full bg-white/10 hover:bg-white/20 text-white"
              onClick={() => setShowUploadModal(true)}
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
            >
              <FiCamera className="w-5 h-5" />
            </motion.button>
            {picture && (
              <>
                <motion.button
                  className="p-2 rounded-full bg-white/10 hover:bg-white/20 text-white"
                  onClick={() => setShowFullscreen(true)}
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                >
                  <FiMaximize className="w-5 h-5" />
                </motion.button>
                <motion.button
                  className="p-2 rounded-full bg-white/10 hover:bg-white/20 text-white"
                  onClick={handleDelete}
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  disabled={isDeleting}
                >
                  <FiTrash2 className="w-5 h-5" />
                </motion.button>
              </>
            )}
          </div>
        </div>
      </div>

      <AnimatePresence>
        {showUploadModal && (
          <motion.div
            className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <motion.div
              className="bg-white rounded-lg p-6 max-w-lg w-full mx-auto"
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
            >
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-semibold">Update Profile Picture</h3>
                <button
                  onClick={() => setShowUploadModal(false)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  <FiX className="w-5 h-5" />
                </button>
              </div>

              <ProfilePictureUpload
                onUpload={handleUpload}
                currentPicture={picture}
                currentThumbnail={thumbnail}
                isUploading={isUploading}
              />
            </motion.div>
          </motion.div>
        )}

        {showFullscreen && picture && (
          <motion.div
            className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-90 p-4"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <motion.div
              className="relative max-w-4xl w-full mx-auto"
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
            >
              <img
                src={picture}
                alt="Profile"
                className="w-full h-auto rounded-lg shadow-xl"
              />
              <div className="absolute top-4 right-4 flex space-x-2">
                <motion.button
                  className="p-2 rounded-full bg-white/10 hover:bg-white/20 text-white"
                  onClick={() => setShowFullscreen(false)}
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                >
                  <FiX className="w-5 h-5" />
                </motion.button>
                {onDelete && (
                  <motion.button
                    className="p-2 rounded-full bg-white/10 hover:bg-white/20 text-white"
                    onClick={handleDelete}
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    disabled={isDeleting}
                  >
                    <FiTrash2 className="w-5 h-5" />
                  </motion.button>
                )}
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default ProfilePictureManager; 