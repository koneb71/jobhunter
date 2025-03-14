import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiUser } from 'react-icons/fi';

interface ProfilePictureDisplayProps {
  picture?: string;
  thumbnail?: string;
  size?: 'small' | 'medium' | 'large';
  showPlaceholder?: boolean;
  className?: string;
}

const sizeClasses = {
  small: 'w-8 h-8',
  medium: 'w-12 h-12',
  large: 'w-16 h-16',
};

const ProfilePictureDisplay: React.FC<ProfilePictureDisplayProps> = ({
  picture,
  thumbnail,
  size = 'medium',
  showPlaceholder = true,
  className = '',
}) => {
  const sizeClass = sizeClasses[size];
  const [isLoading, setIsLoading] = useState(true);
  const [showHighRes, setShowHighRes] = useState(false);
  const imageUrl = thumbnail || picture;

  useEffect(() => {
    if (imageUrl) {
      setIsLoading(true);
      const img = new Image();
      img.src = imageUrl;
      img.onload = () => {
        setIsLoading(false);
        if (picture && thumbnail) {
          // Load high-res image after thumbnail
          const highResImg = new Image();
          highResImg.src = picture;
          highResImg.onload = () => {
            setShowHighRes(true);
          };
        }
      };
    }
  }, [imageUrl, picture, thumbnail]);

  return (
    <motion.div
      className={`
        relative rounded-full overflow-hidden
        ${sizeClass}
        ${className}
        bg-gray-100
        shadow-sm
        border-2 border-white
      `}
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.2 }}
    >
      <AnimatePresence mode="wait">
        {isLoading ? (
          <motion.div
            key="loading"
            className="w-full h-full flex items-center justify-center"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <div className="animate-pulse">
              <FiUser className={`${size === 'small' ? 'w-4 h-4' : size === 'medium' ? 'w-6 h-6' : 'w-8 h-8'} text-gray-400`} />
            </div>
          </motion.div>
        ) : imageUrl ? (
          <motion.div
            key="image"
            className="relative w-full h-full"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <motion.img
              src={showHighRes ? picture : imageUrl}
              alt="Profile"
              className="w-full h-full object-cover"
              initial={{ scale: 1.1 }}
              animate={{ scale: 1 }}
              transition={{ duration: 0.3 }}
              loading="lazy"
            />
            {showHighRes && (
              <motion.div
                className="absolute inset-0 bg-gradient-to-t from-black/10 to-transparent"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.3 }}
              />
            )}
          </motion.div>
        ) : showPlaceholder ? (
          <motion.div
            key="placeholder"
            className="w-full h-full flex items-center justify-center"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <FiUser className={`${size === 'small' ? 'w-4 h-4' : size === 'medium' ? 'w-6 h-6' : 'w-8 h-8'} text-gray-400`} />
          </motion.div>
        ) : null}
      </AnimatePresence>
    </motion.div>
  );
};

export default ProfilePictureDisplay; 