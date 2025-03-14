import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Briefcase, MapPin, Clock, DollarSign, Building2, ExternalLink } from 'lucide-react';
import jobService from '../../services/jobService';
import { toast } from 'react-hot-toast';

interface JobDetailsProps {
  jobId?: string;
}

const JobDetails: React.FC<JobDetailsProps> = ({ jobId: propJobId }) => {
  const { jobId: urlJobId } = useParams<{ jobId: string }>();
  const navigate = useNavigate();
  const [job, setJob] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isApplying, setIsApplying] = useState(false);

  const id = propJobId || urlJobId;

  useEffect(() => {
    const fetchJobDetails = async () => {
      if (!id) {
        toast.error('No job ID provided');
        navigate('/jobs');
        return;
      }

      try {
        const jobData = await jobService.getJobById(id);
        setJob(jobData);
      } catch (error) {
        toast.error('Failed to load job details');
        console.error('Error loading job details:', error);
        navigate('/jobs');
      } finally {
        setIsLoading(false);
      }
    };

    fetchJobDetails();
  }, [id, navigate]);

  const handleApply = async () => {
    if (!job) return;
    
    setIsApplying(true);
    try {
      await jobService.applyForJob(job.id);
      toast.success('Application submitted successfully!');
      navigate('/applications');
    } catch (error) {
      toast.error('Failed to submit application');
      console.error('Error applying for job:', error);
    } finally {
      setIsApplying(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-1/4 mb-4"></div>
            <div className="h-4 bg-gray-200 rounded w-1/2 mb-8"></div>
            <div className="space-y-4">
              <div className="h-4 bg-gray-200 rounded w-3/4"></div>
              <div className="h-4 bg-gray-200 rounded w-1/2"></div>
              <div className="h-4 bg-gray-200 rounded w-2/3"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!job) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="bg-white rounded-lg shadow-lg p-6 mb-8"
        >
          <div className="flex justify-between items-start mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">{job.title}</h1>
              <div className="flex items-center text-gray-600">
                <Building2 className="h-5 w-5 mr-2" />
                <span>{job.company}</span>
              </div>
            </div>
            <div className="flex space-x-4">
              <button
                onClick={handleApply}
                disabled={isApplying}
                className="inline-flex items-center px-6 py-2 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isApplying ? 'Applying...' : 'Apply Now'}
              </button>
              <a
                href={job.apply_url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                <ExternalLink className="h-4 w-4 mr-2" />
                External Apply
              </a>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="flex items-center text-gray-600">
              <MapPin className="h-5 w-5 mr-2" />
              <span>{job.location}</span>
            </div>
            <div className="flex items-center text-gray-600">
              <Briefcase className="h-5 w-5 mr-2" />
              <span>{job.job_type}</span>
            </div>
            <div className="flex items-center text-gray-600">
              <Clock className="h-5 w-5 mr-2" />
              <span>{job.experience_level}</span>
            </div>
            <div className="flex items-center text-gray-600">
              <DollarSign className="h-5 w-5 mr-2" />
              <span>{job.salary_range}</span>
            </div>
          </div>

          <div className="prose max-w-none">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Job Description</h2>
            <div className="text-gray-600 whitespace-pre-wrap">{job.description}</div>

            <h2 className="text-xl font-semibold text-gray-900 mt-8 mb-4">Requirements</h2>
            <ul className="list-disc pl-5 text-gray-600">
              {job.requirements.map((req: string, index: number) => (
                <li key={index}>{req}</li>
              ))}
            </ul>

            <h2 className="text-xl font-semibold text-gray-900 mt-8 mb-4">Benefits</h2>
            <ul className="list-disc pl-5 text-gray-600">
              {job.benefits.map((benefit: string, index: number) => (
                <li key={index}>{benefit}</li>
              ))}
            </ul>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default JobDetails; 