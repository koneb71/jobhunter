import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { fetchWithAuth } from '@/utils/api';

export interface User {
  id: string;
  email: string;
  display_name: string;
  user_type: string;
  is_active: boolean;
  created_at: string;
}

export function useUsers() {
  const queryClient = useQueryClient();

  const { data: users, isLoading, error } = useQuery<User[]>({
    queryKey: ['users'],
    queryFn: async () => {
      const data = await fetchWithAuth('/users');
      return data;
    },
  });

  const deleteUser = useMutation({
    mutationFn: async (userId: string) => {
      await fetchWithAuth(`/users/${userId}`, {
        method: 'DELETE',
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });

  const updateUser = useMutation({
    mutationFn: async ({ userId, data }: { userId: string; data: Partial<User> }) => {
      const response = await fetchWithAuth(`/users/${userId}`, {
        method: 'PATCH',
        body: JSON.stringify(data),
      });
      return response;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });

  return {
    users,
    isLoading,
    error,
    deleteUser: deleteUser.mutate,
    updateUser: updateUser.mutate,
    isDeletingUser: deleteUser.isPending,
    isUpdatingUser: updateUser.isPending,
  };
} 