<script setup lang="ts">
import { onBeforeUnmount, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { fetchCamp } from '../api/catalog'
import { parseCampSlug } from '../lib/camp'
import NotFoundView from '../views/NotFoundView.vue'

const route = useRoute()
const ready = ref(false)
const missing = ref(false)

const applyCamp = (slug: string | null) => {
  if (slug) {
    document.documentElement.dataset.camp = slug
    return
  }
  delete document.documentElement.dataset.camp
}

const load = async () => {
  const slug = parseCampSlug(route.params.campSlug)
  if (!slug) {
    missing.value = true
    ready.value = true
    applyCamp(null)
    return
  }
  ready.value = false
  missing.value = false
  try {
    await fetchCamp(slug)
    applyCamp(slug)
    missing.value = false
  } catch {
    applyCamp(null)
    missing.value = true
  } finally {
    ready.value = true
  }
}

watch(
  () => route.params.campSlug,
  () => {
    void load()
  },
  { immediate: true },
)

onBeforeUnmount(() => {
  applyCamp(null)
})
</script>

<template>
  <NotFoundView v-if="ready && missing" />
  <router-view v-else-if="ready" />
</template>
