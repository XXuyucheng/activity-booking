import { api } from './http'

export type BookingResponse = {
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
  status: string
  created_at: string
}

export type CreateBookingBody = {
  schedule_id: string
  contact_name: string
  contact_phone: string
  adult_count: number
  child_count: number
  remark: string
}

export const fetchBookings = () => api<BookingResponse[]>('/api/bookings')

export const fetchBooking = (id: string) =>
  api<BookingResponse>(`/api/bookings/${id}`)

export const createBooking = (body: CreateBookingBody) =>
  api<BookingResponse>('/api/bookings', {
    method: 'POST',
    body: JSON.stringify(body),
  })

export const cancelBooking = (id: string) =>
  api<BookingResponse>(`/api/bookings/${id}/cancel`, { method: 'POST' })
