import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { toast } from 'react-hot-toast'
import { useAuthStore } from '@/stores/authStore'
import { validatePassword } from '@/utils/passwordValidation'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { Progress } from '@/components/ui/progress'
import { Loader2 } from 'lucide-react'

export function RegisterForm() {
  const navigate = useNavigate()
  const { register, isLoading, error } = useAuthStore()
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    first_name: '',
    last_name: '',
    display_name: '',
    user_type: 'job_seeker' as 'job_seeker' | 'employer',
  })
  const [passwordStrength, setPasswordStrength] = useState({
    score: 0,
    isStrong: false,
    feedback: [] as string[]
  })

  useEffect(() => {
    if (formData.password) {
      setPasswordStrength(validatePassword(formData.password))
    } else {
      setPasswordStrength({ score: 0, isStrong: false, feedback: [] })
    }
  }, [formData.password])

  useEffect(() => {
    if (!formData.display_name.trim() && formData.first_name.trim() && formData.last_name.trim()) {
      setFormData(prev => ({
        ...prev,
        display_name: `${prev.first_name.trim()} ${prev.last_name.trim()}`
      }))
    }
  }, [formData.first_name, formData.last_name])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    // Validate first name and last name
    if (!formData.first_name.trim()) {
      toast.error('First name is required')
      return
    }
    if (!formData.last_name.trim()) {
      toast.error('Last name is required')
      return
    }

    if (!passwordStrength.isStrong) {
      toast.error('Please choose a stronger password')
      return
    }

    if (formData.password !== formData.confirmPassword) {
      toast.error('Passwords do not match')
      return
    }

    try {
      const { confirmPassword, ...registerData } = formData
      // Only include display_name if it's not empty
      const data = {
        ...registerData,
        display_name: registerData.display_name.trim() || undefined
      }
      await register(data)
      toast.success('Registration successful!')
      navigate('/dashboard')
    } catch (err) {
      // Error is handled by the store
      console.error('Registration error:', err)
    }
  }

  const getPasswordStrengthColor = () => {
    switch (passwordStrength.score) {
      case 0:
        return 'bg-red-500'
      case 1:
        return 'bg-red-500'
      case 2:
        return 'bg-yellow-500'
      case 3:
        return 'bg-yellow-500'
      case 4:
      case 5:
        return 'bg-green-500'
      default:
        return 'bg-gray-200'
    }
  }

  return (
    <Card className="w-[400px]">
      <CardHeader>
        <CardTitle>Create an Account</CardTitle>
        <CardDescription>
          Sign up to start your job search or hire talent
        </CardDescription>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent className="space-y-4">
          {error && (
            <div className="text-sm text-red-500 dark:text-red-400">
              {error}
            </div>
          )}
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              name="email"
              type="email"
              placeholder="Enter your email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="first_name">First Name</Label>
              <Input
                id="first_name"
                name="first_name"
                placeholder="First name"
                value={formData.first_name}
                onChange={handleChange}
                required
                minLength={2}
                maxLength={50}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="last_name">Last Name</Label>
              <Input
                id="last_name"
                name="last_name"
                placeholder="Last name"
                value={formData.last_name}
                onChange={handleChange}
                required
                minLength={2}
                maxLength={50}
              />
            </div>
          </div>
          <div className="space-y-2">
            <Label htmlFor="display_name">Display Name (Optional)</Label>
            <Input
              id="display_name"
              name="display_name"
              placeholder="How would you like to be displayed? (e.g., John Doe, John D., etc.)"
              value={formData.display_name}
              onChange={handleChange}
              maxLength={100}
            />
            <p className="text-sm text-muted-foreground">
              If left empty, your full name will be used
            </p>
          </div>
          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              name="password"
              type="password"
              placeholder="Create a password"
              value={formData.password}
              onChange={handleChange}
              required
            />
            {formData.password && (
              <div className="space-y-2">
                <Progress
                  value={(passwordStrength.score / 5) * 100}
                  className={getPasswordStrengthColor()}
                />
                {passwordStrength.feedback.length > 0 && (
                  <ul className="text-sm text-muted-foreground space-y-1">
                    {passwordStrength.feedback.map((feedback, index) => (
                      <li key={index}>{feedback}</li>
                    ))}
                  </ul>
                )}
              </div>
            )}
          </div>
          <div className="space-y-2">
            <Label htmlFor="confirmPassword">Confirm Password</Label>
            <Input
              id="confirmPassword"
              name="confirmPassword"
              type="password"
              placeholder="Confirm your password"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
            />
          </div>
          <div className="space-y-2">
            <Label>I am a</Label>
            <RadioGroup
              value={formData.user_type}
              onValueChange={(value) => setFormData(prev => ({ ...prev, user_type: value as 'job_seeker' | 'employer' }))}
              className="flex space-x-4"
            >
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="job_seeker" id="job_seeker" />
                <Label htmlFor="job_seeker">Job Seeker</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="employer" id="employer" />
                <Label htmlFor="employer">Employer</Label>
              </div>
            </RadioGroup>
          </div>
        </CardContent>
        <CardFooter className="flex justify-between">
          <Button
            type="button"
            variant="outline"
            onClick={() => navigate('/login')}
          >
            Already have an account
          </Button>
          <Button
            type="submit"
            disabled={isLoading || !passwordStrength.isStrong}
          >
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Creating account...
              </>
            ) : (
              'Sign Up'
            )}
          </Button>
        </CardFooter>
      </form>
    </Card>
  )
} 