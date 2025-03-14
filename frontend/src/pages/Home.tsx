import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import axios from 'axios'

interface Job {
  id: string
  title: string
  company: string
  location: string
  salary: string
  type: string
  description: string
}

const Home = () => {
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
    // Implement search functionality
  }

  return (
    <div className="bg-white">
      {/* Hero section */}
      <div className="relative isolate overflow-hidden bg-gradient-to-b from-primary-100/20">
        <div className="mx-auto max-w-7xl pb-24 pt-10 sm:pb-32 lg:grid lg:grid-cols-2 lg:gap-x-8 lg:px-8 lg:py-40">
          <div className="px-6 lg:px-0 lg:pt-4">
            <div className="mx-auto max-w-2xl">
              <div className="max-w-lg">
                <h1 className="mt-10 text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
                  Find your dream job today
                </h1>
                <p className="mt-6 text-lg leading-8 text-gray-600">
                  Connect with top employers and discover opportunities that match your skills and aspirations.
                </p>
                <div className="mt-10 flex items-center gap-x-6">
                  <Link
                    to="/jobs"
                    className="rounded-md bg-primary-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600"
                  >
                    Browse Jobs
                  </Link>
                  <Link
                    to="/register"
                    className="text-sm font-semibold leading-6 text-gray-900"
                  >
                    Create an account <span aria-hidden="true">→</span>
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Search section */}
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 -mt-10">
        <div className="mx-auto max-w-2xl rounded-lg bg-white shadow-xl ring-1 ring-gray-900/10">
          <form onSubmit={handleSearch} className="p-6">
            <div className="grid grid-cols-1 gap-x-6 gap-y-4 sm:grid-cols-2">
              <div>
                <label
                  htmlFor="search"
                  className="block text-sm font-medium leading-6 text-gray-900"
                >
                  What
                </label>
                <div className="mt-2">
                  <input
                    type="text"
                    name="search"
                    id="search"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6"
                    placeholder="Job title, keywords, or company"
                  />
                </div>
              </div>
              <div>
                <label
                  htmlFor="location"
                  className="block text-sm font-medium leading-6 text-gray-900"
                >
                  Where
                </label>
                <div className="mt-2">
                  <input
                    type="text"
                    name="location"
                    id="location"
                    value={location}
                    onChange={(e) => setLocation(e.target.value)}
                    className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6"
                    placeholder="City, state, or zip code"
                  />
                </div>
              </div>
            </div>
            <div className="mt-6">
              <button
                type="submit"
                className="w-full rounded-md bg-primary-600 px-3.5 py-2.5 text-center text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600"
              >
                Search
              </button>
            </div>
          </form>
        </div>
      </div>

      {/* Featured jobs section */}
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-24">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            Featured Jobs
          </h2>
          <p className="mt-2 text-lg leading-8 text-gray-600">
            Discover the latest opportunities from top companies
          </p>
        </div>
        <div className="mx-auto mt-16 grid max-w-2xl grid-cols-1 gap-x-8 gap-y-20 lg:mx-0 lg:max-w-none lg:grid-cols-3">
          {isLoading ? (
            <div className="col-span-3 text-center">Loading...</div>
          ) : (
            featuredJobs?.map((job) => (
              <article
                key={job.id}
                className="flex flex-col items-start justify-between"
              >
                <div className="relative w-full">
                  <h3 className="mt-3 text-lg font-semibold leading-6 text-gray-900">
                    <Link to={`/jobs/${job.id}`}>
                      <span className="absolute inset-0" />
                      {job.title}
                    </Link>
                  </h3>
                  <p className="mt-5 line-clamp-3 text-sm leading-6 text-gray-600">
                    {job.description}
                  </p>
                </div>
                <div className="relative mt-8 flex items-center gap-x-4">
                  <div className="text-sm leading-6">
                    <p className="font-semibold text-gray-900">
                      <span className="absolute inset-0" />
                      {job.company}
                    </p>
                    <p className="text-gray-600">{job.location}</p>
                  </div>
                </div>
                <div className="mt-4 flex items-center gap-x-4 text-xs">
                  <span className="rounded-full bg-primary-50 px-2 py-1 text-primary-700">
                    {job.type}
                  </span>
                  <span className="text-gray-500">{job.salary}</span>
                </div>
              </article>
            ))
          )}
        </div>
      </div>
    </div>
  )
}

export default Home 