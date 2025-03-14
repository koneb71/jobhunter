import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import { Toaster } from 'react-hot-toast'
import { useAuthStore } from '@/stores/authStore'
import Login from '@/pages/auth/Login'
import { RegisterPage } from '@/pages/auth/RegisterPage'
import { Dashboard } from '@/pages/dashboard/Dashboard'

// Layouts
import MainLayout from './layouts/MainLayout'
import AuthLayout from './layouts/AuthLayout'
import { AdminLayout } from './layouts/AdminLayout'

// Pages
import Home from './pages/Home'
import JobSearch from './pages/jobs/JobSearch'
import JobDetails from './pages/jobs/JobDetails'
import Profile from './pages/profile/Profile'
import CompanyProfile from './pages/company/CompanyProfile'

// Admin Pages
import AdminDashboard from './pages/admin/Dashboard'
import AdminUsers from './pages/admin/Users'
import AdminJobs from './pages/admin/Jobs'
import AdminAnalytics from './pages/admin/Analytics'
import AdminSettings from './pages/admin/Settings'

const queryClient = new QueryClient()

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuthStore()
  return isAuthenticated ? children : <Navigate to="/login" />
}

function AdminRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, user } = useAuthStore()
  return isAuthenticated && user?.user_type === 'admin' ? (
    children
  ) : (
    <Navigate to="/dashboard" />
  )
}

function PublicRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuthStore()
  return !isAuthenticated ? children : <Navigate to="/dashboard" />
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Toaster position="top-right" />
        <Routes>
          <Route path="/" element={<MainLayout />}>
            <Route index element={<Home />} />
            <Route path="jobs" element={<JobSearch />} />
            <Route path="jobs/:id" element={<JobDetails />} />
            <Route path="profile" element={<PrivateRoute><Profile /></PrivateRoute>} />
            <Route path="company/:id" element={<CompanyProfile />} />
          </Route>

          <Route path="/" element={<AuthLayout />}>
            <Route path="login" element={<Login />} />
            <Route path="register" element={<RegisterPage />} />
          </Route>

          {/* Protected routes */}
          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                <Dashboard />
              </PrivateRoute>
            }
          />

          {/* Admin routes */}
          <Route
            element={
              <AdminRoute>
                <AdminLayout />
              </AdminRoute>
            }
          >
            <Route path="/admin/dashboard" element={<AdminDashboard />} />
            <Route path="/admin/users" element={<AdminUsers />} />
            <Route path="/admin/jobs" element={<AdminJobs />} />
            <Route path="/admin/analytics" element={<AdminAnalytics />} />
            <Route path="/admin/settings" element={<AdminSettings />} />
          </Route>
        </Routes>
      </Router>
      <ToastContainer position="top-right" />
    </QueryClientProvider>
  )
}

export default App 