import React from "react"
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom"
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import { Toaster } from "@/components/ui/toaster"
import { useAuthStore } from "@/stores/auth"
import Login from "@/pages/auth/Login"
import RegisterPage from "@/pages/auth/RegisterPage"
import AdminDashboard from "@/pages/admin/Dashboard"
import EmployerDashboard from "@/pages/employer/Dashboard"
import JobSeekerDashboard from "@/pages/jobseeker/Dashboard"
import { PostJob } from '@/pages/employer/PostJob'

// Layouts
import MainLayout from "@/layouts/MainLayout"
import AuthLayout from "@/layouts/AuthLayout"
import { AdminLayout } from "@/layouts/AdminLayout"

// Pages
import Home from "@/pages/Home"
// import JobSearch from './pages/jobs/JobSearch'
// import JobDetails from './pages/jobs/JobDetails'
// import Profile from './pages/profile/Profile'
// import CompanyProfile from './pages/company/CompanyProfile'

// Admin Pages
import AdminUsers from './pages/admin/Users'
import AdminJobs from './pages/admin/Jobs'
import AdminAnalytics from './pages/admin/Analytics'
import AdminSettings from './pages/admin/Settings'

const queryClient = new QueryClient()

// Route protection components
const PrivateRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated } = useAuthStore()
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />
}

const AdminRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated, user } = useAuthStore()
  return isAuthenticated && user?.user_type === "admin" ? (
    <>{children}</>
  ) : (
    <Navigate to="/" />
  )
}

const EmployerRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated, user } = useAuthStore()
  return isAuthenticated && user?.user_type === "employer" ? (
    <>{children}</>
  ) : (
    <Navigate to="/" />
  )
}

const JobSeekerRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated, user } = useAuthStore()
  return isAuthenticated && user?.user_type === "job_seeker" ? (
    <>{children}</>
  ) : (
    <Navigate to="/" />
  )
}

// Dashboard redirect component
const DashboardRedirect = () => {
  const { user } = useAuthStore()
  
  if (!user) return <Navigate to="/login" />
  
  switch (user.user_type) {
    case "admin":
      return <Navigate to="/admin/dashboard" />
    case "employer":
      return <Navigate to="/employer/dashboard" />
    case "job_seeker":
      return <Navigate to="/job-seeker/dashboard" />
    default:
      return <Navigate to="/dashboard" />
  }
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Toaster />
        <Routes>
          {/* Public routes */}
          <Route
            path="/"
            element={
              <MainLayout>
                <Home />
              </MainLayout>
            }
          />
          <Route
            path="/login"
            element={
              <AuthLayout>
                <Login />
              </AuthLayout>
            }
          />
          <Route
            path="/register"
            element={
              <AuthLayout>
                <RegisterPage />
              </AuthLayout>
            }
          />

          {/* Protected routes */}
          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                <MainLayout>
                  <DashboardRedirect />
                </MainLayout>
              </PrivateRoute>
            }
          />

          {/* Role-specific routes */}
          <Route
            path="/admin/*"
            element={
              <AdminRoute>
                <AdminLayout>
                  <Routes>
                    <Route path="dashboard" element={<AdminDashboard />} />
                    <Route path="users" element={<AdminUsers />} />
                    <Route path="jobs" element={<AdminJobs />} />
                    <Route path="analytics" element={<AdminAnalytics />} />
                    <Route path="settings" element={<AdminSettings />} />
                  </Routes>
                </AdminLayout>
              </AdminRoute>
            }
          />

          <Route
            path="/employer/*"
            element={
              <EmployerRoute>
                <MainLayout>
                  <Routes>
                    <Route path="dashboard" element={<EmployerDashboard />} />
                    <Route path="post-job" element={<PostJob />} />
                  </Routes>
                </MainLayout>
              </EmployerRoute>
            }
          />

          <Route
            path="/job-seeker/*"
            element={
              <JobSeekerRoute>
                <MainLayout>
                  <Routes>
                    <Route path="dashboard" element={<JobSeekerDashboard />} />
                  </Routes>
                </MainLayout>
              </JobSeekerRoute>
            }
          />

          {/* Catch all route - redirect to appropriate dashboard */}
          <Route
            path="*"
            element={
              <PrivateRoute>
                <DashboardRedirect />
              </PrivateRoute>
            }
          />
        </Routes>
      </Router>
      <ToastContainer position="top-right" />
    </QueryClientProvider>
  )
}

export default App 