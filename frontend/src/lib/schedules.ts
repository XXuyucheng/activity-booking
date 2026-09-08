import type { ScheduleResponse } from '../api/catalog'

const TZ = 'Asia/Shanghai'
const WEEKDAYS = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']

export type ScheduleSlot = {
  scheduleId: string
  time: string
  booked: number
  capacity: number
  remaining: number
}

export type DateSession = {
  date: string
  weekday: string
  slots: ScheduleSlot[]
}

const partsInShanghai = (iso: string) => {
  const date = new Date(iso)
  const fmt = new Intl.DateTimeFormat('en-US', {
    timeZone: TZ,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hourCycle: 'h23',
  })
  const bag: Record<string, string> = {}
  for (const part of fmt.formatToParts(date)) {
    if (part.type !== 'literal') bag[part.type] = part.value
  }
  return {
    date: `${bag.year}-${bag.month}-${bag.day}`,
    time: `${bag.hour}:${bag.minute}`,
  }
}

const weekdayLabel = (iso: string) => {
  const local = new Date(
    new Date(iso).toLocaleString('en-US', { timeZone: TZ }),
  )
  return WEEKDAYS[local.getDay()] ?? ''
}

export const groupSchedules = (
  schedules: ScheduleResponse[],
): DateSession[] => {
  const byDate = new Map<string, DateSession>()
  for (const item of schedules) {
    const start = partsInShanghai(item.start_time)
    const end = partsInShanghai(item.end_time)
    let session = byDate.get(start.date)
    if (!session) {
      session = {
        date: start.date,
        weekday: weekdayLabel(item.start_time),
        slots: [],
      }
      byDate.set(start.date, session)
    }
    session.slots.push({
      scheduleId: item.id,
      time: `${start.time}–${end.time}`,
      booked: item.booked_count,
      capacity: item.capacity,
      remaining: item.remaining,
    })
  }
  return [...byDate.values()].map((session) => ({
    ...session,
    slots: session.slots.sort((a, b) => a.time.localeCompare(b.time)),
  }))
}

export const slotRemaining = (slot: ScheduleSlot) => slot.remaining

export const isSlotFull = (slot: ScheduleSlot) => slot.remaining <= 0

export const sessionBooked = (session: DateSession) =>
  session.slots.reduce((sum, slot) => sum + slot.booked, 0)

export const sessionCapacity = (session: DateSession) =>
  session.slots.reduce((sum, slot) => sum + slot.capacity, 0)

export const isSessionFull = (session: DateSession) =>
  session.slots.every(isSlotFull)

export const formatClockRange = (startIso: string, endIso: string) => {
  const start = partsInShanghai(startIso)
  const end = partsInShanghai(endIso)
  const [, month, day] = start.date.split('-')
  return `${Number(month)}月${Number(day)}日 ${weekdayLabel(startIso)} · ${start.time}–${end.time}`
}

export const formatDateTime = (iso: string) => {
  const { date, time } = partsInShanghai(iso)
  return `${date} ${time}`
}
