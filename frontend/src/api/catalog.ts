import { CAMP_SLUG } from '../constants'
import { api } from './http'

export type CampResponse = {
  id: string
  slug: string
  name: string
  description: string
  status: string
}

export type ActivityListItem = {
  id: string
  name: string
  cover: string
  duration: number | null
  price: string
  child_price: string
  status: 'open' | 'full'
}

export type ScheduleResponse = {
  id: string
  start_time: string
  end_time: string
  capacity: number
  booked_count: number
  remaining: number
  status: string
}

export type ActivityDetailResponse = ActivityListItem & {
  description: string
  notice: string
  schedules: ScheduleResponse[]
}

export const fetchCamp = (slug = CAMP_SLUG) =>
  api<CampResponse>(`/api/camps/${slug}`)

export const fetchCampActivities = (slug = CAMP_SLUG) =>
  api<ActivityListItem[]>(`/api/camps/${slug}/activities`)

export const fetchActivity = (id: string) =>
  api<ActivityDetailResponse>(`/api/activities/${id}`)
