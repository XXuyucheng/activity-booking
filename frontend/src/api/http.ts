import { campSlugFromPath } from '../lib/camp'

export class ApiError extends Error {
  readonly status: number

  constructor(message: string, status: number) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

export const redirectToLogin = () => {
  const slug = campSlugFromPath(window.location.pathname)
  window.location.assign(`/api/auth/wechat/start?camp=${encodeURIComponent(slug)}`)
}

const parseDetail = (body: unknown): string => {
  if (!body || typeof body !== 'object') return '请求失败'
  const detail = (body as { detail?: unknown }).detail
  if (typeof detail === 'string' && detail.trim()) return detail
  if (Array.isArray(detail) && detail[0] && typeof detail[0] === 'object') {
    const first = detail[0] as { msg?: unknown }
    if (typeof first.msg === 'string' && first.msg.trim()) return first.msg
  }
  return '请求失败'
}

export const api = async <T>(path: string, init: RequestInit = {}): Promise<T> => {
  const headers = new Headers(init.headers)
  if (init.body && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json')
  }
  const response = await fetch(path, {
    ...init,
    credentials: 'include',
    headers,
  })
  if (response.status === 204) {
    return undefined as T
  }
  const text = await response.text()
  let data: unknown = null
  if (text) {
    try {
      data = JSON.parse(text) as unknown
    } catch {
      data = text
    }
  }
  if (!response.ok) {
    throw new ApiError(parseDetail(data), response.status)
  }
  return data as T
}
