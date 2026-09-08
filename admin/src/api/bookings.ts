import { api } from './http'

export type BookingStatus = 'pending' | 'contacted' | 'expired'

export type AdminBooking = {
  id: string
  activity_id: string
  activity_name: string
  schedule_id: string
  start_time: string
  end_time: string
  contact_name: string
  contact_phone: string
  adult_count: number
  child_count: number
  remark: string
  total_price: string
  status: BookingStatus
  created_at: string
}

export const listBookings = (status?: BookingStatus | '') => {
  const query = status ? `?status=${encodeURIComponent(status)}` : ''
  return api<AdminBooking[]>(`/api/admin/bookings${query}`)
}

export const markContacted = (bookingId: string) =>
  api<AdminBooking>(`/api/admin/bookings/${bookingId}/contact`, {
    method: 'POST',
  })

export const cancelBooking = (bookingId: string) =>
  api<AdminBooking>(`/api/admin/bookings/${bookingId}/cancel`, {
    method: 'POST',
  })
