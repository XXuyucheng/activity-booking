import { parseCampSlug } from './camp'

const STORAGE_KEY = 'ab_oauth_return'
const MAX_AGE_MS = 10 * 60 * 1000
const ACTIVITY_PATH_RE =
  /^\/([a-z0-9-]{1,64})\/activity\/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$/i
const SCHEDULE_ID_RE =
  /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i

export type OAuthReturn = {
  path: string
  scheduleId: string
}

type StoredReturn = OAuthReturn & { at: number }

const memory = (): Storage | null => {
  try {
    return window.sessionStorage
  } catch {
    return null
  }
}

export const isOAuthReturnTarget = (path: string, scheduleId: string): boolean => {
  const match = ACTIVITY_PATH_RE.exec(path)
  if (!match || parseCampSlug(match[1]) !== match[1]) return false
  return SCHEDULE_ID_RE.test(scheduleId)
}

export const saveOAuthReturn = (path: string, scheduleId: string): boolean => {
  if (!isOAuthReturnTarget(path, scheduleId)) return false
  const store = memory()
  if (!store) return false
  const payload: StoredReturn = { path, scheduleId, at: Date.now() }
  store.setItem(STORAGE_KEY, JSON.stringify(payload))
  return true
}

export const peekOAuthReturn = (): OAuthReturn | null => {
  const store = memory()
  if (!store) return null
  const raw = store.getItem(STORAGE_KEY)
  if (!raw) return null
  let parsed: unknown
  try {
    parsed = JSON.parse(raw) as unknown
  } catch {
    store.removeItem(STORAGE_KEY)
    return null
  }
  if (!parsed || typeof parsed !== 'object') {
    store.removeItem(STORAGE_KEY)
    return null
  }
  const record = parsed as Partial<StoredReturn>
  const fresh =
    typeof record.at === 'number' &&
    record.at <= Date.now() + 60_000 &&
    Date.now() - record.at <= MAX_AGE_MS
  if (
    typeof record.path !== 'string' ||
    typeof record.scheduleId !== 'string' ||
    !fresh ||
    !isOAuthReturnTarget(record.path, record.scheduleId)
  ) {
    store.removeItem(STORAGE_KEY)
    return null
  }
  return { path: record.path, scheduleId: record.scheduleId }
}

export const clearOAuthReturn = (): void => {
  memory()?.removeItem(STORAGE_KEY)
}
