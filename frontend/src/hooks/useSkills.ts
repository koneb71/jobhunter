import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { fetchWithAuth } from '@/utils/api';

export interface Skill {
  id: number;
  name: string;
  description: string | null;
  category: string | null;
  created_at: string;
  updated_at: string | null;
}

export interface CreateSkillData {
  name: string;
  description?: string;
  category?: string;
}

export const useSkills = () => {
  const queryClient = useQueryClient();

  const { data: skills = [], isLoading } = useQuery<Skill[]>({
    queryKey: ['skills'],
    queryFn: async () => {
      const response = await fetchWithAuth('/skills');
      return response.json();
    },
  });

  const createSkill = useMutation({
    mutationFn: async (skillData: CreateSkillData) => {
      const response = await fetchWithAuth('/skills', {
        method: 'POST',
        body: JSON.stringify(skillData),
      });
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['skills'] });
    },
  });

  const getOrCreateSkill = async (name: string): Promise<Skill> => {
    const existingSkill = skills.find(
      (skill) => skill.name.toLowerCase() === name.toLowerCase()
    );
    
    if (existingSkill) {
      return existingSkill;
    }

    const newSkill = await createSkill.mutateAsync({
      name,
      category: 'Other',
    });

    return newSkill;
  };

  return {
    skills,
    isLoading,
    createSkill,
    getOrCreateSkill,
  };
}; 