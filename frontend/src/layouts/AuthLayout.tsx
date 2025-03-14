import { Outlet } from 'react-router-dom'
import Navbar from '../components/Navbar'

interface AuthLayoutProps {
  children?: React.ReactNode
}

const AuthLayout = ({ children }: AuthLayoutProps) => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="flex flex-col justify-center py-12 sm:px-6 lg:px-8">
        <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
          <div className="bg-white px-4 py-8 shadow sm:rounded-lg sm:px-10">
            {children || <Outlet />}
          </div>
        </div>
      </div>
    </div>
  )
}

export default AuthLayout 