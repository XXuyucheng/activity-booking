import activityCover from '../assets/activity-cover.png'

export type ActivityStatus = 'open' | 'ongoing' | 'full'

export type Camp = {
  name: string
  location: string
  intro: string
}

export type Activity = {
  id: string
  title: string
  session: string
  booked: number
  capacity: number
  status: ActivityStatus
  cover: string
}

export const camp: Camp = {
  name: '松间营地',
  location: '浙江 · 莫干山',
  intro: '林间木屋与夜读灯火。从公众号进入，预约本营本期活动。',
}

export const activities: Activity[] = [
  {
    id: 'a1',
    title: '松间夜读',
    session: '8 月 23 日 19:00–21:00',
    booked: 12,
    capacity: 20,
    status: 'open',
    cover: activityCover,
  },
  {
    id: 'a2',
    title: '晨雾徒步',
    session: '8 月 24 日 06:30–09:00',
    booked: 8,
    capacity: 16,
    status: 'ongoing',
    cover: activityCover,
  },
  {
    id: 'a3',
    title: '林火料理课',
    session: '8 月 25 日 16:00–18:30',
    booked: 12,
    capacity: 12,
    status: 'full',
    cover: activityCover,
  },
]
