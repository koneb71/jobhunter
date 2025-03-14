import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { fetchWithAuth } from '@/utils/api';

export interface Benefit {
  id: number;
  name: string;
  description: string | null;
  category: string | null;
  created_at: string;
  updated_at: string | null;
}

export interface CreateBenefitData {
  name: string;
  description?: string;
  category?: string;
}

export const useBenefits = () => {
  const queryClient = useQueryClient();

  const { data: benefits = [], isLoading } = useQuery<Benefit[]>({
    queryKey: ['benefits'],
    queryFn: async () => {
      const response = await fetchWithAuth('/benefits');
      return response.json();
    },
  });

  const createBenefit = useMutation({
    mutationFn: async (benefitData: CreateBenefitData) => {
      const response = await fetchWithAuth('/benefits', {
        method: 'POST',
        body: JSON.stringify(benefitData),
      });
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['benefits'] });
    },
  });

  const getOrCreateBenefit = async (name: string): Promise<Benefit> => {
    const existingBenefit = benefits.find(
      (benefit) => benefit.name.toLowerCase() === name.toLowerCase()
    );
    
    if (existingBenefit) {
      return existingBenefit;
    }

    const newBenefit = await createBenefit.mutateAsync({
      name,
      category: 'Other',
    });

    return newBenefit;
  };

  return {
    benefits,
    isLoading,
    createBenefit,
    getOrCreateBenefit,
  };
}; 