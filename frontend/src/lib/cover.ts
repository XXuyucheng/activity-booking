import activityCover from '../assets/activity-cover.png'
import activityCoverPearl from '../assets/activity-cover-pearl.png'
import kaodigua from '../assets/kaodigua.webp'

const COVERS: Record<string, string> = {
  'activity-cover.png': activityCover,
  'activity-cover-pearl.png': activityCoverPearl,
  'kaodigua.webp': kaodigua,
}

export const coverUrl = (cover: string) => COVERS[cover] ?? activityCover
