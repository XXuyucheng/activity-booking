export type BookingStatus = 'pending' | 'contacted' | 'expired'

export type BookingRecord = {
  id: string
  activityId: string
  title: string
  sessionLabel: string
  name: string
  count: number
  childCount: number
  phone: string
  remark: string
  totalPrice: number
  status: BookingStatus
  createdAt: number
}

const STORAGE_KEY = 'ab-bookings'

const normalize = (item: Partial<BookingRecord>): BookingRecord => ({
  id: item.id ?? `${Date.now()}`,
  activityId: item.activityId ?? '',
  title: item.title ?? '',
  sessionLabel: item.sessionLabel ?? '',
  name: item.name ?? '',
  count: item.count ?? 1,
  childCount: item.childCount ?? 0,
  phone: item.phone ?? '',
  remark: item.remark ?? '',
  totalPrice: item.totalPrice ?? 0,
  status: item.status ?? 'pending',
  createdAt: item.createdAt ?? 0,
})

export const loadBookings = (): BookingRecord[] => {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return []
    const parsed = JSON.parse(raw)
    if (!Array.isArray(parsed)) return []
    return parsed.map((item) => normalize(item as Partial<BookingRecord>))
  } catch {
    return []
  }
}

export const saveBooking = (record: BookingRecord) => {
  const list = loadBookings()
  list.unshift(record)
  localStorage.setItem(STORAGE_KEY, JSON.stringify(list))
}

export const getBookingById = (id: string) =>
  loadBookings().find((item) => item.id === id)

export const updateBookingStatus = (id: string, status: BookingStatus) => {
  const list = loadBookings()
  const next = list.map((item) =>
    item.id === id ? { ...item, status } : item,
  )
  localStorage.setItem(STORAGE_KEY, JSON.stringify(next))
}
