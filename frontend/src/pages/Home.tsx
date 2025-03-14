import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import axios from 'axios'
import { motion } from 'framer-motion'
import { Search, MapPin, Briefcase, ChevronRight, Star } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

interface Job {
  id: string
  title: string
  company: string
  location: string
  salary: string
  type: string
  description: string
  companyLogo: string
  rating: string
}

const Home = () => {
  const navigate = useNavigate()
  const [searchQuery, setSearchQuery] = useState('')
  const [location, setLocation] = useState('')

  const { data: featuredJobs, isLoading } = useQuery<Job[]>({
    queryKey: ['featuredJobs'],
    queryFn: async () => {
      const response = await axios.get('/api/v1/jobs/featured')
      return response.data
    },
  })

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    navigate(`/jobs?q=${searchQuery}&location=${location}`)
  }

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="relative bg-white">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-24 md:py-32">
          <div className="text-center">
            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="text-4xl md:text-6xl font-bold tracking-tight text-gray-900 sm:text-5xl"
            >
              Find your dream<br />job today
            </motion.h1>
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
              className="mt-6 text-lg leading-8 text-gray-600 max-w-2xl mx-auto"
            >
              Connect with top employers and discover opportunities that
              match your skills and aspirations.
            </motion.p>
          </div>

          {/* Search Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="mt-10 max-w-3xl mx-auto"
          >
            <form onSubmit={handleSearch} className="flex flex-col md:flex-row gap-4">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                <Input
                  type="text"
                  placeholder="Job title, keywords, or company"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10 w-full"
                />
              </div>
              <div className="flex-1 relative">
                <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                <Input
                  type="text"
                  placeholder="City, state, or zip code"
                  value={location}
                  onChange={(e) => setLocation(e.target.value)}
                  className="pl-10 w-full"
                />
              </div>
              <Button type="submit" className="md:w-auto">
                Search Jobs
              </Button>
            </form>
          </motion.div>
        </div>
      </div>

      {/* Featured Categories */}
      <div className="bg-gray-50 py-16 sm:py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
              Popular Job Categories
            </h2>
            <p className="mt-4 text-lg text-gray-600">
              Explore opportunities across various industries
            </p>
          </div>

          <div className="mt-12 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
            {categories.map((category) => (
              <motion.div
                key={category.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="relative group rounded-xl border border-gray-200 bg-white p-6 hover:border-blue-500 hover:shadow-lg transition-all duration-200"
                onClick={() => navigate(`/jobs?category=${category.title.toLowerCase()}`)}
              >
                <div className="flex items-center gap-4">
                  <div className={`p-3 rounded-lg ${category.bgColor}`}>
                    {category.icon}
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 group-hover:text-blue-500">
                      {category.title}
                    </h3>
                    <p className="mt-1 text-sm text-gray-500">
                      {category.jobCount} open positions
                    </p>
                  </div>
                </div>
                <ChevronRight className="absolute right-6 top-1/2 transform -translate-y-1/2 text-gray-400 group-hover:text-blue-500 h-5 w-5" />
              </motion.div>
            ))}
          </div>
        </div>
      </div>

      {/* Featured Jobs */}
      <div className="bg-white py-16 sm:py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center">
            <div>
              <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
                Featured Jobs
              </h2>
              <p className="mt-4 text-lg text-gray-600">
                Discover the latest opportunities from top companies
              </p>
            </div>
            <Button variant="outline" onClick={() => navigate('/jobs')}>
              View all jobs
            </Button>
          </div>

          <div className="mt-12 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
            {isLoading ? (
              <div className="col-span-3 text-center">Loading...</div>
            ) : (
              featuredJobs?.map((job) => (
                <motion.div
                  key={job.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5 }}
                  className="relative rounded-xl border border-gray-200 bg-white p-6 hover:shadow-lg transition-all duration-200"
                  onClick={() => navigate(`/jobs/${job.id}`)}
                >
                  <div className="flex items-start gap-4">
                    <img
                      src={job.companyLogo}
                      alt={job.company}
                      className="h-12 w-12 rounded-lg object-contain bg-gray-50 p-2"
                    />
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">
                        {job.title}
                      </h3>
                      <p className="mt-1 text-sm text-gray-500">
                        {job.company}
                      </p>
                      <div className="mt-2 flex items-center gap-2 text-sm text-gray-500">
                        <MapPin className="h-4 w-4" />
                        {job.location}
                      </div>
                      <div className="mt-4 flex items-center gap-4">
                        <span className="inline-flex items-center rounded-full bg-blue-50 px-2 py-1 text-xs font-medium text-blue-700">
                          {job.type}
                        </span>
                        <span className="inline-flex items-center text-sm text-gray-500">
                          <Star className="h-4 w-4 text-yellow-400 mr-1" />
                          {job.rating}
                        </span>
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

const categories = [
  {
    title: 'Technology',
    icon: <Briefcase className="h-6 w-6 text-blue-600" />,
    bgColor: 'bg-blue-50',
    jobCount: '1.2k'
  },
  {
    title: 'Design',
    icon: <Briefcase className="h-6 w-6 text-purple-600" />,
    bgColor: 'bg-purple-50',
    jobCount: '840'
  },
  {
    title: 'Marketing',
    icon: <Briefcase className="h-6 w-6 text-green-600" />,
    bgColor: 'bg-green-50',
    jobCount: '650'
  },
  {
    title: 'Finance',
    icon: <Briefcase className="h-6 w-6 text-yellow-600" />,
    bgColor: 'bg-yellow-50',
    jobCount: '920'
  },
  {
    title: 'Healthcare',
    icon: <Briefcase className="h-6 w-6 text-red-600" />,
    bgColor: 'bg-red-50',
    jobCount: '760'
  },
  {
    title: 'Education',
    icon: <Briefcase className="h-6 w-6 text-indigo-600" />,
    bgColor: 'bg-indigo-50',
    jobCount: '540'
  }
]

export default Home 