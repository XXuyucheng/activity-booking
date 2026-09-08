import { api } from './http'

export type MeResponse = {
  id: string | null
  logged_in: boolean
}

export const fetchMe = () => api<MeResponse>('/api/auth/me')
