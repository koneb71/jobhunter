import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuthStore } from '@/stores/auth';

const Dashboard: React.FC = () => {
  const { user } = useAuthStore();

  // Redirect based on user type
  switch (user?.type) {
    case 'admin':
      return <Navigate to="/admin/dashboard" replace />;
    case 'employer':
      return <Navigate to="/employer/dashboard" replace />;
    case 'jobseeker':
      return <Navigate to="/job-seeker/dashboard" replace />;
    default:
      return <Navigate to="/login" replace />;
  }
};

export default Dashboard; 