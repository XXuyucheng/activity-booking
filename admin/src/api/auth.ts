import { api } from './http'

export type StaffMe = {
  id: string
  username: string
  camp_id: string
  camp_slug: string
  camp_name: string
}

export const fetchMe = () => api<StaffMe>('/api/admin/me')

export const login = (username: string, password: string) =>
  api<StaffMe>('/api/admin/login', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  })

export const logout = () =>
  api<void>('/api/admin/logout', {
    method: 'POST',
  })
