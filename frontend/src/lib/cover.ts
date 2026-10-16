import activityCover from '../assets/activity-cover.png'
import activityCoverPearl from '../assets/activity-cover-pearl.png'
import kaodigua from '../assets/kaodigua.webp'
import tuanshan from '../assets/tuanshan.webp'
import wuhuanzi from '../assets/wuhuanzi.webp'
import lollipop from '../assets/lollipop.webp'

const COVERS: Record<string, string> = {
  'activity-cover.png': activityCover,
  'activity-cover-pearl.png': activityCoverPearl,
  'kaodigua.webp': kaodigua,
  'tuanshan.webp': tuanshan,
  'wuhuanzi.webp': wuhuanzi,
  'lollipop.webp': lollipop,
}

export const coverUrl = (cover: string) => COVERS[cover] ?? activityCover
