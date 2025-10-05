import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import axios from 'axios';

const API = '/api/pedidos';

export function usePedidos() {
  return useQuery({
    queryKey: ['pedidos'],
    queryFn: async () => (await axios.get(API)).data,
  });
}

export function useCrearPedido() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (nuevo: any) => axios.post(API, nuevo),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['pedidos'] }),
  });
}

export function useAgregarLineaPedido() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, linea }: any) => axios.post(`${API}/${id}/lineas`, linea),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['pedidos'] }),
  });
}

export function useConfirmarPedido() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => axios.post(`${API}/${id}/confirmar`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['pedidos'] }),
  });
}

export function useCancelarPedido() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => axios.post(`${API}/${id}/cancelar`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['pedidos'] }),
  });
}
