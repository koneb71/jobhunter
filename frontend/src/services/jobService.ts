import axios from 'axios';
import { API_URL } from '../config';

export interface JobSearchParams {
  query?: string;
  location?: string;
  job_type?: string;
  experience_level?: string;
  salary_range?: string;
  date_posted?: string;
  page?: number;
  limit?: number;
}

export interface Job {
  id: string;
  title: string;
  company: string;
  location: string;
  job_type: string;
  description: string;
  requirements: string[];
  salary_range: {
    min: number;
    max: number;
    currency: string;
  };
  experience_level: string;
  posted_at: string;
  deadline: string;
  company_logo?: string;
  is_active: boolean;
}

export interface JobSearchResponse {
  jobs: Job[];
  total: number;
  page: number;
  total_pages: number;
}

const jobService = {
  async searchJobs(params: JobSearchParams): Promise<JobSearchResponse> {
    const response = await axios.get(`${API_URL}/jobs/search`, { params });
    return response.data;
  },

  async getJobById(id: string): Promise<Job> {
    const response = await axios.get(`${API_URL}/jobs/${id}`);
    return response.data;
  },

  async getJobTypes(): Promise<string[]> {
    const response = await axios.get(`${API_URL}/jobs/types`);
    return response.data;
  },

  async getExperienceLevels(): Promise<string[]> {
    const response = await axios.get(`${API_URL}/jobs/experience-levels`);
    return response.data;
  },

  async getSalaryRanges(): Promise<string[]> {
    const response = await axios.get(`${API_URL}/jobs/salary-ranges`);
    return response.data;
  }
};

export default jobService; 