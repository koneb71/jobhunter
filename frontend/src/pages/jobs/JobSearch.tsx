import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, MapPin, Briefcase, Filter, Clock, X, Check } from 'lucide-react';
import jobService, { JobSearchParams, Job } from '../../services/jobService';
import searchService, { SearchHistoryItem, JobSuggestion } from '../../services/searchService';
import { toast } from 'react-hot-toast';
import { useDebounce } from '../../hooks/useDebounce';

interface JobSearchProps {
  onSearch?: (query: string) => void;
  userId?: string;
}

const JobSearch: React.FC<JobSearchProps> = ({ onSearch, userId }) => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [location, setLocation] = useState('');
  const [jobType, setJobType] = useState('all');
  const [isFilterOpen, setIsFilterOpen] = useState(false);
  const [experienceLevel, setExperienceLevel] = useState('');
  const [salaryRange, setSalaryRange] = useState('');
  const [datePosted, setDatePosted] = useState('');
  const [jobTypes, setJobTypes] = useState<string[]>([]);
  const [experienceLevels, setExperienceLevels] = useState<string[]>([]);
  const [salaryRanges, setSalaryRanges] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  const [locationSuggestions, setLocationSuggestions] = useState<string[]>([]);
  const [jobSuggestions, setJobSuggestions] = useState<JobSuggestion[]>([]);
  const [selectedSkills, setSelectedSkills] = useState<string[]>([]);
  const [selectedIndustries, setSelectedIndustries] = useState<string[]>([]);
  const [selectedBenefits, setSelectedBenefits] = useState<string[]>([]);
  const [selectedWorkEnvironments, setSelectedWorkEnvironments] = useState<string[]>([]);
  const [searchHistory, setSearchHistory] = useState<SearchHistoryItem[]>([]);
  const debouncedLocation = useDebounce(location, 300);
  const locationRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const fetchFilterOptions = async () => {
      try {
        const [types, levels, ranges] = await Promise.all([
          jobService.getJobTypes(),
          jobService.getExperienceLevels(),
          jobService.getSalaryRanges()
        ]);
        setJobTypes(types);
        setExperienceLevels(levels);
        setSalaryRanges(ranges);
      } catch (error) {
        toast.error('Failed to load filter options');
        console.error('Error loading filter options:', error);
      }
    };

    fetchFilterOptions();
    setSearchHistory(searchService.getSearchHistory());
  }, []);

  useEffect(() => {
    const fetchLocationSuggestions = async () => {
      if (debouncedLocation.length >= 2) {
        const suggestions = await searchService.getLocationSuggestions(debouncedLocation);
        setLocationSuggestions(suggestions);
      } else {
        setLocationSuggestions([]);
      }
    };

    fetchLocationSuggestions();
  }, [debouncedLocation]);

  useEffect(() => {
    const fetchJobSuggestions = async () => {
      if (userId) {
        const suggestions = await searchService.getJobSuggestions(userId);
        setJobSuggestions(suggestions);
      }
    };

    fetchJobSuggestions();
  }, [userId]);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (locationRef.current && !locationRef.current.contains(event.target as Node)) {
        setLocationSuggestions([]);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const searchParams: JobSearchParams = {
        query: searchQuery,
        location,
        job_type: jobType !== 'all' ? jobType : undefined,
        experience_level: experienceLevel || undefined,
        salary_range: salaryRange || undefined,
        date_posted: datePosted || undefined,
        skills: selectedSkills.length > 0 ? selectedSkills : undefined,
        industries: selectedIndustries.length > 0 ? selectedIndustries : undefined,
        benefits: selectedBenefits.length > 0 ? selectedBenefits : undefined,
        work_environments: selectedWorkEnvironments.length > 0 ? selectedWorkEnvironments : undefined,
        page: 1,
        limit: 10
      };

      const response = await jobService.searchJobs(searchParams);
      
      if (onSearch) {
        onSearch(searchQuery);
      }

      searchService.addToSearchHistory(searchParams);
      setSearchHistory(searchService.getSearchHistory());

      navigate(`/jobs/search?${new URLSearchParams(searchParams as any).toString()}`);
    } catch (error) {
      toast.error('Failed to search jobs');
      console.error('Error searching jobs:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleHistoryItemClick = (item: SearchHistoryItem) => {
    setSearchQuery(item.params.query || '');
    setLocation(item.params.location || '');
    setJobType(item.params.job_type || 'all');
    setExperienceLevel(item.params.experience_level || '');
    setSalaryRange(item.params.salary_range || '');
    setDatePosted(item.params.date_posted || '');
    setSelectedSkills(item.params.skills || []);
    setSelectedIndustries(item.params.industries || []);
    setSelectedBenefits(item.params.benefits || []);
    setSelectedWorkEnvironments(item.params.work_environments || []);
    setShowHistory(false);
  };

  const handleClearHistory = () => {
    searchService.clearSearchHistory();
    setSearchHistory([]);
  };

  const toggleSkill = (skill: string) => {
    setSelectedSkills(prev =>
      prev.includes(skill)
        ? prev.filter(s => s !== skill)
        : [...prev, skill]
    );
  };

  const toggleIndustry = (industry: string) => {
    setSelectedIndustries(prev =>
      prev.includes(industry)
        ? prev.filter(i => i !== industry)
        : [...prev, industry]
    );
  };

  const toggleBenefit = (benefit: string) => {
    setSelectedBenefits(prev =>
      prev.includes(benefit)
        ? prev.filter(b => b !== benefit)
        : [...prev, benefit]
    );
  };

  const toggleWorkEnvironment = (environment: string) => {
    setSelectedWorkEnvironments(prev =>
      prev.includes(environment)
        ? prev.filter(e => e !== environment)
        : [...prev, environment]
    );
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Find Your Dream Job
          </h1>
          <p className="text-xl text-gray-600">
            Search through thousands of job opportunities
          </p>
        </motion.div>

        <motion.form
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          onSubmit={handleSearch}
          className="bg-white rounded-lg shadow-lg p-6 mb-8"
        >
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search className="h-5 w-5 text-gray-400" />
              </div>
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Job title, keywords, or company"
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              />
            </div>

            <div className="relative" ref={locationRef}>
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <MapPin className="h-5 w-5 text-gray-400" />
              </div>
              <input
                type="text"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                placeholder="Location"
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              />
              {locationSuggestions.length > 0 && (
                <div className="absolute z-10 w-full mt-1 bg-white rounded-md shadow-lg">
                  <ul className="py-1">
                    {locationSuggestions.map((suggestion, index) => (
                      <li
                        key={index}
                        className="px-4 py-2 hover:bg-gray-100 cursor-pointer"
                        onClick={() => {
                          setLocation(suggestion);
                          setLocationSuggestions([]);
                        }}
                      >
                        {suggestion}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Briefcase className="h-5 w-5 text-gray-400" />
              </div>
              <select
                value={jobType}
                onChange={(e) => setJobType(e.target.value)}
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              >
                <option value="all">All Types</option>
                {jobTypes.map((type) => (
                  <option key={type} value={type}>
                    {type}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="mt-4 flex justify-between items-center">
            <div className="flex space-x-4">
              <button
                type="button"
                onClick={() => setIsFilterOpen(!isFilterOpen)}
                className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                <Filter className="h-4 w-4 mr-2" />
                More Filters
              </button>

              <button
                type="button"
                onClick={() => setShowHistory(!showHistory)}
                className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                <Clock className="h-4 w-4 mr-2" />
                Search History
              </button>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="inline-flex items-center px-6 py-2 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Searching...' : 'Search Jobs'}
            </button>
          </div>
        </motion.form>

        <AnimatePresence>
          {showHistory && searchHistory.length > 0 && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="bg-white rounded-lg shadow-lg p-6 mb-8"
            >
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-medium text-gray-900">Recent Searches</h3>
                <button
                  onClick={handleClearHistory}
                  className="text-sm text-red-600 hover:text-red-800"
                >
                  Clear History
                </button>
              </div>
              <ul className="space-y-2">
                {searchHistory.map((item, index) => (
                  <li
                    key={index}
                    onClick={() => handleHistoryItemClick(item)}
                    className="p-3 hover:bg-gray-50 rounded-md cursor-pointer"
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="font-medium">
                          {item.params.query || 'No query'}
                        </p>
                        <p className="text-sm text-gray-500">
                          {item.params.location && `${item.params.location} • `}
                          {item.params.job_type && item.params.job_type !== 'all' && item.params.job_type}
                        </p>
                      </div>
                      <span className="text-sm text-gray-500">
                        {new Date(item.timestamp).toLocaleDateString()}
                      </span>
                    </div>
                  </li>
                ))}
              </ul>
            </motion.div>
          )}
        </AnimatePresence>

        {jobSuggestions.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-lg shadow-lg p-6 mb-8"
          >
            <h3 className="text-lg font-medium text-gray-900 mb-4">Recommended for You</h3>
            <div className="space-y-4">
              {jobSuggestions.map((suggestion) => (
                <div
                  key={suggestion.id}
                  className="p-4 border rounded-lg hover:border-blue-500 cursor-pointer"
                  onClick={() => navigate(`/jobs/${suggestion.id}`)}
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <h4 className="font-medium">{suggestion.title}</h4>
                      <p className="text-sm text-gray-500">{suggestion.company}</p>
                    </div>
                    <div className="text-sm text-blue-600">
                      {Math.round(suggestion.match_score * 100)}% Match
                    </div>
                  </div>
                  <p className="text-sm text-gray-600 mt-2">{suggestion.reason}</p>
                </div>
              ))}
            </div>
          </motion.div>
        )}

        {isFilterOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="bg-white rounded-lg shadow-lg p-6 mb-8"
          >
            <h3 className="text-lg font-medium text-gray-900 mb-4">Additional Filters</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-medium text-gray-700 mb-2">Experience Level</h4>
                <select
                  value={experienceLevel}
                  onChange={(e) => setExperienceLevel(e.target.value)}
                  className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
                >
                  <option value="">Any Level</option>
                  {experienceLevels.map((level) => (
                    <option key={level} value={level}>
                      {level}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <h4 className="font-medium text-gray-700 mb-2">Salary Range</h4>
                <select
                  value={salaryRange}
                  onChange={(e) => setSalaryRange(e.target.value)}
                  className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
                >
                  <option value="">Any Range</option>
                  {salaryRanges.map((range) => (
                    <option key={range} value={range}>
                      {range}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <h4 className="font-medium text-gray-700 mb-2">Date Posted</h4>
                <select
                  value={datePosted}
                  onChange={(e) => setDatePosted(e.target.value)}
                  className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
                >
                  <option value="">Any Time</option>
                  <option value="24h">Last 24 hours</option>
                  <option value="7d">Last 7 days</option>
                  <option value="30d">Last 30 days</option>
                  <option value="90d">Last 90 days</option>
                </select>
              </div>

              <div>
                <h4 className="font-medium text-gray-700 mb-2">Work Environment</h4>
                <div className="flex flex-wrap gap-2">
                  {searchService.getAdvancedFilters().workEnvironments.map((env) => (
                    <button
                      key={env}
                      onClick={() => toggleWorkEnvironment(env)}
                      className={`inline-flex items-center px-3 py-1 rounded-full text-sm ${
                        selectedWorkEnvironments.includes(env)
                          ? 'bg-blue-100 text-blue-800'
                          : 'bg-gray-100 text-gray-800'
                      }`}
                    >
                      {env}
                      {selectedWorkEnvironments.includes(env) && (
                        <X className="h-3 w-3 ml-1" />
                      )}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <h4 className="font-medium text-gray-700 mb-2">Skills</h4>
                <div className="flex flex-wrap gap-2">
                  {searchService.getAdvancedFilters().skills.map((skill) => (
                    <button
                      key={skill}
                      onClick={() => toggleSkill(skill)}
                      className={`inline-flex items-center px-3 py-1 rounded-full text-sm ${
                        selectedSkills.includes(skill)
                          ? 'bg-blue-100 text-blue-800'
                          : 'bg-gray-100 text-gray-800'
                      }`}
                    >
                      {skill}
                      {selectedSkills.includes(skill) && (
                        <X className="h-3 w-3 ml-1" />
                      )}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <h4 className="font-medium text-gray-700 mb-2">Industries</h4>
                <div className="flex flex-wrap gap-2">
                  {searchService.getAdvancedFilters().industries.map((industry) => (
                    <button
                      key={industry}
                      onClick={() => toggleIndustry(industry)}
                      className={`inline-flex items-center px-3 py-1 rounded-full text-sm ${
                        selectedIndustries.includes(industry)
                          ? 'bg-blue-100 text-blue-800'
                          : 'bg-gray-100 text-gray-800'
                      }`}
                    >
                      {industry}
                      {selectedIndustries.includes(industry) && (
                        <X className="h-3 w-3 ml-1" />
                      )}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <h4 className="font-medium text-gray-700 mb-2">Benefits</h4>
                <div className="flex flex-wrap gap-2">
                  {searchService.getAdvancedFilters().benefits.map((benefit) => (
                    <button
                      key={benefit}
                      onClick={() => toggleBenefit(benefit)}
                      className={`inline-flex items-center px-3 py-1 rounded-full text-sm ${
                        selectedBenefits.includes(benefit)
                          ? 'bg-blue-100 text-blue-800'
                          : 'bg-gray-100 text-gray-800'
                      }`}
                    >
                      {benefit}
                      {selectedBenefits.includes(benefit) && (
                        <X className="h-3 w-3 ml-1" />
                      )}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default JobSearch; 