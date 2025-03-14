interface PasswordStrength {
  score: number // 0-4
  isStrong: boolean
  feedback: string[]
}

export function validatePassword(password: string): PasswordStrength {
  const feedback: string[] = []
  let score = 0

  // Length check
  if (password.length < 8) {
    feedback.push('Password should be at least 8 characters long')
  } else {
    score += 1
  }

  // Uppercase check
  if (!/[A-Z]/.test(password)) {
    feedback.push('Include at least one uppercase letter')
  } else {
    score += 1
  }

  // Lowercase check
  if (!/[a-z]/.test(password)) {
    feedback.push('Include at least one lowercase letter')
  } else {
    score += 1
  }

  // Number check
  if (!/\d/.test(password)) {
    feedback.push('Include at least one number')
  } else {
    score += 1
  }

  // Special character check
  if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
    feedback.push('Include at least one special character')
  } else {
    score += 1
  }

  return {
    score,
    isStrong: score >= 4,
    feedback
  }
} 