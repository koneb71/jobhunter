import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Eye, EyeOff } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Checkbox } from '@/components/ui/checkbox'
import { useAuthStore } from '@/stores/authStore'
import { toast } from 'react-hot-toast'

const Login = () => {
  const navigate = useNavigate()
  const { login } = useAuthStore()
  const [isLoading, setIsLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    remember: false
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleCheckboxChange = (checked: boolean) => {
    setFormData(prev => ({
      ...prev,
      remember: checked
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    try {
      setIsLoading(true)
      const userType = await login(formData.email, formData.password, formData.remember)
      toast.success('Login successful!')
      
      // Redirect based on user type
      switch (userType) {
        case 'admin':
          navigate('/admin/dashboard')
          break
        case 'employer':
          navigate('/employer/dashboard')
          break
        case 'job_seeker':
          navigate('/job-seeker/dashboard')
          break
        default:
          navigate('/dashboard')
      }
    } catch (error) {
      toast.error('Invalid email or password')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex flex-col items-center justify-center bg-gray-50">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-sm px-8 py-10 bg-white rounded-lg shadow-sm"
      >
        <div className="text-center mb-6">
          <h1 className="text-2xl font-bold text-gray-900">Welcome Back</h1>
          <p className="mt-1 text-sm text-gray-600">Sign in to continue your job search</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Label htmlFor="email" className="text-sm">Email</Label>
            <Input
              id="email"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="Enter your email"
              required
              className="mt-1"
            />
          </div>

          <div>
            <Label htmlFor="password" className="text-sm">Password</Label>
            <div className="relative mt-1">
              <Input
                id="password"
                name="password"
                type={showPassword ? 'text' : 'password'}
                value={formData.password}
                onChange={handleChange}
                placeholder="Enter your password"
                required
                className="pr-10"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                {showPassword ? (
                  <EyeOff className="h-4 w-4" />
                ) : (
                  <Eye className="h-4 w-4" />
                )}
              </button>
            </div>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Checkbox
                id="remember"
                checked={formData.remember}
                onCheckedChange={handleCheckboxChange}
                className="h-4 w-4 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
              />
              <Label
                htmlFor="remember"
                className="text-sm text-gray-700 cursor-pointer"
              >
                Remember me
              </Label>
            </div>

            <Link
              to="/forgot-password"
              className="text-sm font-medium text-primary-600 hover:text-primary-500"
            >
              Forgot password?
            </Link>
          </div>

          <Button
            type="submit"
            disabled={isLoading}
            className="w-full"
          >
            {isLoading ? 'Signing in...' : 'Sign in'}
          </Button>

          <div className="text-center text-sm text-gray-600">
            Don't have an account?{' '}
            <Link
              to="/register"
              className="font-medium text-primary-600 hover:text-primary-500"
            >
              Sign up
            </Link>
          </div>
        </form>
      </motion.div>
    </div>
  )
}

export default Login 