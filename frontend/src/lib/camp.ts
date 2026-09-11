export const DEFAULT_CAMP_SLUG = 'luhe'

export const CAMP_SLUG_RE = /^[a-z0-9-]{1,64}$/

export const parseCampSlug = (value: unknown): string | null => {
  if (typeof value !== 'string') return null
  const slug = value.trim().toLowerCase()
  return CAMP_SLUG_RE.test(slug) ? slug : null
}

export const campSlugFromPath = (pathname: string): string => {
  const match = pathname.match(/^\/([a-z0-9-]{1,64})(?:\/|$)/)
  const slug = match?.[1]
  if (!slug || slug === 'playground') return DEFAULT_CAMP_SLUG
  return slug
}
