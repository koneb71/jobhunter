const getEnvVar = (key: string): string => {
  const value = import.meta.env[key]
  if (value === undefined) {
    throw new Error(`Environment variable ${key} is not defined`)
  }
  return value
}

export const API_BASE_URL = getEnvVar('VITE_API_BASE_URL')
export const API_VERSION = getEnvVar('VITE_API_VERSION')

export const API_ENDPOINTS = {
  base: `${API_BASE_URL}/api/${API_VERSION}`,
  auth: {
    login: `${API_BASE_URL}/api/${API_VERSION}/auth/login`,
    register: `${API_BASE_URL}/api/${API_VERSION}/auth/register`,
  },
  users: {
    profile: `${API_BASE_URL}/api/${API_VERSION}/users/profile`,
  },
  jobs: {
    list: `${API_BASE_URL}/api/${API_VERSION}/jobs`,
    create: `${API_BASE_URL}/api/${API_VERSION}/jobs`,
    details: (id: string) => `${API_BASE_URL}/api/${API_VERSION}/jobs/${id}`,
  },
} 