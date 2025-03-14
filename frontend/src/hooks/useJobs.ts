import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { fetchWithAuth } from '@/utils/api';

export interface Job {
  id: string;
  title: string;
  company: string;
  location: string;
  type: string;
  salary_min: number;
  salary_max: number;
  description: string;
  requirements: string;
  responsibilities: string;
  benefits: string;
  experience_level: string;
  education_level: string;
  skills: string[];
  created_at: string;
  updated_at: string;
  employer_id: string;
  status: 'draft' | 'published' | 'closed';
}

export interface PaginatedJobs {
  items: Job[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface JobsQueryParams {
  page?: number;
  size?: number;
}

export interface CreateJobData {
  title: string;
  description: string;
  company_id: string;
  location: string;
  salary_range: string;
  employment_type: string;
  experience_level: string;
  skills_required: string[];
  benefits: string[];
  is_remote: boolean;
  is_featured: boolean;
  status: string;
  department: string;
  remote_work: boolean;
  visa_sponsorship: boolean;
  relocation_assistance: boolean;
}

export function useJobs(params: JobsQueryParams = { page: 1, size: 10 }) {
  const queryClient = useQueryClient();

  const { data, isLoading, error } = useQuery<PaginatedJobs>({
    queryKey: ['jobs', params],
    queryFn: async () => {
      const searchParams = new URLSearchParams();
      if (params.page) searchParams.append('page', params.page.toString());
      if (params.size) searchParams.append('size', params.size.toString());
      
      const data = await fetchWithAuth(`/jobs?${searchParams.toString()}`);
      return data;
    },
  });

  const createJob = useMutation({
    mutationFn: async (jobData: CreateJobData) => {
      const response = await fetchWithAuth('/jobs', {
        method: 'POST',
        body: JSON.stringify(jobData),
      });
      return response;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['jobs'] });
    },
  });

  const updateJob = useMutation({
    mutationFn: async ({ jobId, data }: { jobId: string; data: Partial<Job> }) => {
      const response = await fetchWithAuth(`/jobs/${jobId}`, {
        method: 'PATCH',
        body: JSON.stringify(data),
      });
      return response;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['jobs'] });
    },
  });

  const deleteJob = useMutation({
    mutationFn: async (jobId: string) => {
      await fetchWithAuth(`/jobs/${jobId}`, {
        method: 'DELETE',
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['jobs'] });
    },
  });

  return {
    jobs: data?.items ?? [],
    pagination: {
      total: data?.total ?? 0,
      page: data?.page ?? 1,
      size: data?.size ?? 10,
      pages: data?.pages ?? 1,
    },
    isLoading,
    error,
    createJob: createJob.mutate,
    updateJob: updateJob.mutate,
    deleteJob: deleteJob.mutate,
    isCreatingJob: createJob.isPending,
    isUpdatingJob: updateJob.isPending,
    isDeletingJob: deleteJob.isPending,
  };
} 