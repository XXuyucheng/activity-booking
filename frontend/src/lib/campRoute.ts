import { useRoute, useRouter } from 'vue-router'
import { computed } from 'vue'
import { DEFAULT_CAMP_SLUG, parseCampSlug } from './camp'

export const useCampSlug = () => {
  const route = useRoute()
  const campSlug = computed(
    () => parseCampSlug(route.params.campSlug) ?? DEFAULT_CAMP_SLUG,
  )
  return { campSlug }
}

export const useCampRouter = () => {
  const router = useRouter()
  const { campSlug } = useCampSlug()

  const withCamp = (
    name: string,
    params: Record<string, string> = {},
    query?: Record<string, string>,
  ) => ({
    name,
    params: { campSlug: campSlug.value, ...params },
    ...(query ? { query } : {}),
  })

  return {
    campSlug,
    push: (
      name: string,
      params?: Record<string, string>,
      query?: Record<string, string>,
    ) => router.push(withCamp(name, params, query)),
    replace: (
      name: string,
      params?: Record<string, string>,
      query?: Record<string, string>,
    ) => router.replace(withCamp(name, params, query)),
    router,
  }
}
