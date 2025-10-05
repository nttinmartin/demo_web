import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

const API = '/api/ajustes';

export function useAjustes() {
  return useQuery({
    queryKey: ['ajustes'],
    queryFn: async () => (await axios.get(API)).data,
  });
}

// Para métricas de dashboard, puedes crear otro hook similar consultando el endpoint correspondiente
