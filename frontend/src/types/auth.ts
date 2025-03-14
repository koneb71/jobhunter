export interface LoginResponse {
  user: {
    id: string
    email: string
    user_type: 'admin' | 'employer' | 'job_seeker'
    name: string
  }
  access_token: string
}

export interface LoginError {
  detail?: string
  message?: string
  errors?: {
    [key: string]: string[]
  }
} 