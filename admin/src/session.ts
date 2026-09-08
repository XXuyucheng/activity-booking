import { ref } from 'vue'
import type { StaffMe } from './api/auth'

export const currentStaff = ref<StaffMe | null>(null)
