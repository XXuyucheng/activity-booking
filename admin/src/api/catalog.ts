import { api } from './http'

export type AdminScheduleBooking = {
  id: string
  contact_name: string
  contact_phone: string
  adult_count: number
  child_count: number
  status: string
  start_time: string
  end_time: string
  total_price: string
  unpaid_amount: string
}

export type AdminSchedule = {
  id: string
  start_time: string
  end_time: string
  capacity: number
  booked_count: number
  remaining: number
  status: string
  bookings: AdminScheduleBooking[]
  revenue: string
}

export type AdminActivity = {
  id: string
  name: string
  duration: number | null
  price: string
  child_price: string
  schedules: AdminSchedule[]
}

export const listAdminActivities = () => api<AdminActivity[]>('/api/admin/activities')

export const updateActivityPrices = (activityId: string, price: string, childPrice: string) =>
  api<AdminActivity>(`/api/admin/activities/${activityId}`, {
    method: 'POST',
    body: JSON.stringify({ price, child_price: childPrice }),
  })

export const updateSchedule = (
  scheduleId: string,
  payload: { capacity?: number; status?: 'open' | 'closed' },
) =>
  api<AdminActivity>(`/api/admin/schedules/${scheduleId}`, {
    method: 'POST',
    body: JSON.stringify(payload),
  })
