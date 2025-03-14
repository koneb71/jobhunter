const API_VERSION = import.meta.env.VITE_API_VERSION || 'v1';
export const API_URL = `${import.meta.env.VITE_API_URL}/${API_VERSION}`;

export const MAPBOX_TOKEN = import.meta.env.VITE_MAPBOX_TOKEN || '';

export const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB

export const ALLOWED_FILE_TYPES = [
  'application/pdf',
  'application/msword',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
];

export const PAGINATION_LIMIT = 10;

export const JOB_APPLICATION_LIMIT = 50;

export const THEME = {
  colors: {
    primary: '#3B82F6',
    secondary: '#10B981',
    success: '#059669',
    error: '#DC2626',
    warning: '#D97706',
    info: '#3B82F6',
    background: '#F3F4F6',
    surface: '#FFFFFF',
    text: {
      primary: '#111827',
      secondary: '#4B5563',
      disabled: '#9CA3AF',
    },
  },
  spacing: {
    xs: '0.25rem',
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem',
  },
  borderRadius: {
    sm: '0.25rem',
    md: '0.375rem',
    lg: '0.5rem',
    full: '9999px',
  },
  shadows: {
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
  },
}; 