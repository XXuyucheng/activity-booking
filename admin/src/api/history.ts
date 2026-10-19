import { api } from './http'

export type HistoryBooking = {
  id: string
  contact_name: string
  contact_phone: string
  adult_count: number
  child_count: number
  status: string
  total_price: string
  unpaid_amount: string
  remark: string
}

export type HistorySchedule = {
  id: string
  activity_id: string
  activity_name: string
  start_time: string
  end_time: string
  status: string
  bookings: HistoryBooking[]
}

export const listHistory = () => api<HistorySchedule[]>('/api/admin/history')
