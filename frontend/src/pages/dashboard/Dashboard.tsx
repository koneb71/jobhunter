import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  Briefcase,
  Building2,
  FileText,
  Users,
  Settings,
  BarChart,
  Calendar,
  Bell,
  Mail,
  TrendingUp,
  Target,
  PieChart,
  Plus,
  CheckCircle,
  Clock,
  XCircle,
} from 'lucide-react';
import { toast } from 'react-hot-toast';
import {
  AreaChart,
  Area,
  BarChart as RechartsBarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart as RechartsPieChart,
  Pie,
  Cell,
} from 'recharts';
import { useAuthStore } from '@/stores/authStore';
import { fetchWithAuth } from '@/utils/api';

interface DashboardStats {
  total_jobs: number;
  active_jobs: number;
  total_applications: number;
  new_applications: number;
  total_candidates: number;
  new_messages: number;
  new_notifications: number;
  upcoming_interviews: number;
}

interface DashboardJob {
  id: string;
  title: string;
  location: string;
  type: string;
  posted_date: string;
  applications_count: number;
  status: 'active' | 'closed' | 'draft';
}

interface DashboardCandidate {
  id: string;
  name: string;
  position: string;
  experience: string;
  applied_date: string;
  status: 'new' | 'reviewing' | 'interviewing' | 'rejected' | 'accepted';
}

interface ApplicationTrend {
  date: string;
  applications: number;
  interviews: number;
  offers: number;
}

interface JobCategoryDistribution {
  name: string;
  value: number;
}

interface ApplicationStatusDistribution {
  name: string;
  value: number;
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

export const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuthStore();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [activeJobs, setActiveJobs] = useState<DashboardJob[]>([]);
  const [recentCandidates, setRecentCandidates] = useState<DashboardCandidate[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [applicationTrends, setApplicationTrends] = useState<ApplicationTrend[]>([]);
  const [jobCategories, setJobCategories] = useState<JobCategoryDistribution[]>([]);
  const [applicationStatus, setApplicationStatus] = useState<ApplicationStatusDistribution[]>([]);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const data = await fetchWithAuth('/dashboard');
        setStats(data.stats);
        setActiveJobs(data.active_jobs);
        setRecentCandidates(data.recent_candidates);
        setApplicationTrends(data.application_trends);
        setJobCategories(data.job_categories);
        setApplicationStatus(data.application_status);
      } catch (error) {
        toast.error('Failed to load dashboard data');
        console.error('Error loading dashboard:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Employer Dashboard</h1>
        <button
          onClick={() => navigate('/jobs/new')}
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          <Plus className="h-4 w-4 mr-2" />
          Post New Job
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-lg shadow p-6"
        >
          <div className="flex items-center">
            <div className="p-3 bg-blue-100 rounded-full">
              <Briefcase className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Active Jobs</p>
              <p className="text-2xl font-semibold text-gray-900">{stats?.active_jobs}</p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-lg shadow p-6"
        >
          <div className="flex items-center">
            <div className="p-3 bg-green-100 rounded-full">
              <Users className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">New Applications</p>
              <p className="text-2xl font-semibold text-gray-900">{stats?.new_applications}</p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white rounded-lg shadow p-6"
        >
          <div className="flex items-center">
            <div className="p-3 bg-yellow-100 rounded-full">
              <Calendar className="h-6 w-6 text-yellow-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Upcoming Interviews</p>
              <p className="text-2xl font-semibold text-gray-900">{stats?.upcoming_interviews}</p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-white rounded-lg shadow p-6"
        >
          <div className="flex items-center">
            <div className="p-3 bg-purple-100 rounded-full">
              <CheckCircle className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Candidates</p>
              <p className="text-2xl font-semibold text-gray-900">{stats?.total_candidates}</p>
            </div>
          </div>
        </motion.div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5 }}
          className="bg-white rounded-lg shadow p-6"
        >
          <div className="flex items-center mb-4">
            <TrendingUp className="h-5 w-5 text-blue-600 mr-2" />
            <h2 className="text-lg font-medium text-gray-900">Application Trends</h2>
          </div>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={applicationTrends}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Area
                  type="monotone"
                  dataKey="applications"
                  stackId="1"
                  stroke="#8884d8"
                  fill="#8884d8"
                  fillOpacity={0.6}
                />
                <Area
                  type="monotone"
                  dataKey="interviews"
                  stackId="2"
                  stroke="#82ca9d"
                  fill="#82ca9d"
                  fillOpacity={0.6}
                />
                <Area
                  type="monotone"
                  dataKey="offers"
                  stackId="3"
                  stroke="#ffc658"
                  fill="#ffc658"
                  fillOpacity={0.6}
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.6 }}
          className="bg-white rounded-lg shadow p-6"
        >
          <div className="flex items-center mb-4">
            <Target className="h-5 w-5 text-green-600 mr-2" />
            <h2 className="text-lg font-medium text-gray-900">Application Status</h2>
          </div>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <RechartsPieChart>
                <Pie
                  data={applicationStatus}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {applicationStatus.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </RechartsPieChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.7 }}
          className="bg-white rounded-lg shadow"
        >
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-lg font-medium text-gray-900">Active Job Listings</h2>
          </div>
          <div className="p-6">
            <div className="space-y-4">
              {activeJobs.map((job) => (
                <div
                  key={job.id}
                  className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 cursor-pointer"
                  onClick={() => navigate(`/jobs/${job.id}`)}
                >
                  <div>
                    <h3 className="font-medium text-gray-900">{job.title}</h3>
                    <p className="text-sm text-gray-600">{job.location}</p>
                    <p className="text-sm text-gray-500">{job.type}</p>
                  </div>
                  <div className="flex items-center space-x-4">
                    <span className="text-sm text-gray-500">
                      {job.applications_count} applications
                    </span>
                    <span
                      className={`px-2 py-1 rounded-full text-xs font-medium ${
                        job.status === 'active'
                          ? 'bg-green-100 text-green-800'
                          : job.status === 'closed'
                          ? 'bg-red-100 text-red-800'
                          : 'bg-yellow-100 text-yellow-800'
                      }`}
                    >
                      {job.status.charAt(0).toUpperCase() + job.status.slice(1)}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.8 }}
          className="bg-white rounded-lg shadow"
        >
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-lg font-medium text-gray-900">Recent Candidates</h2>
          </div>
          <div className="p-6">
            <div className="space-y-4">
              {recentCandidates.map((candidate) => (
                <div
                  key={candidate.id}
                  className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 cursor-pointer"
                  onClick={() => navigate(`/candidates/${candidate.id}`)}
                >
                  <div>
                    <h3 className="font-medium text-gray-900">{candidate.name}</h3>
                    <p className="text-sm text-gray-600">{candidate.position}</p>
                    <p className="text-sm text-gray-500">{candidate.experience}</p>
                  </div>
                  <div className="flex items-center space-x-4">
                    <span className="text-sm text-gray-500">
                      {new Date(candidate.applied_date).toLocaleDateString()}
                    </span>
                    <span
                      className={`px-2 py-1 rounded-full text-xs font-medium ${
                        candidate.status === 'new'
                          ? 'bg-blue-100 text-blue-800'
                          : candidate.status === 'reviewing'
                          ? 'bg-yellow-100 text-yellow-800'
                          : candidate.status === 'interviewing'
                          ? 'bg-purple-100 text-purple-800'
                          : candidate.status === 'rejected'
                          ? 'bg-red-100 text-red-800'
                          : 'bg-green-100 text-green-800'
                      }`}
                    >
                      {candidate.status.charAt(0).toUpperCase() + candidate.status.slice(1)}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};