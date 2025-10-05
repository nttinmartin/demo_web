import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import axios from 'axios';

const API = '/api/productos';

export function useProductos() {
  return useQuery({
    queryKey: ['productos'],
    queryFn: async () => (await axios.get(API)).data,
  });
}

export function useCrearProducto() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (nuevo: any) => axios.post(API, nuevo),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['productos'] }),
  });
}

export function useActualizarProducto() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...rest }: any) => axios.patch(`${API}/${id}`, rest),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['productos'] }),
  });
}

export function useEliminarProducto() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => axios.delete(`${API}/${id}`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['productos'] }),
  });
}
