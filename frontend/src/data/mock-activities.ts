import activityCover from '../assets/activity-cover.png'
import activityCoverPearl from '../assets/activity-cover-pearl.png'
import kaodigua from '../assets/kaodigua.webp'

export type ActivityStatus = 'open' | 'ongoing' | 'full'

export type CampFacility = {
  name: string
  packId: string | null
  desc: string
}

export type CampPack = {
  id: string
  name: string
  price: number
  unit: string
  summary: string
  includes: string[]
  notes: string
}

export type RuleSection = {
  heading: string
  body: string
}

export type Camp = {
  name: string
  location: string
  intro: string
  story: string
  facilities: CampFacility[]
}

export type ActivitySlot = {
  time: string
  booked: number
  capacity: number
}

export type ActivitySession = {
  date: string
  weekday: string
  slots: ActivitySlot[]
}

export type ActivityDetailSection = {
  heading: string
  body: string
}

export type Activity = {
  id: string
  title: string
  price: number
  childPrice: number
  notice: string
  cover: string
  images: string[]
  intro: string
  tags: string[]
  sessions: ActivitySession[]
  highlights: string[]
  detail: ActivityDetailSection[]
}

export const camp: Camp = {
  name: '麓禾村营地',
  location: '浙江 · 莫干山',
  intro: '麓禾村 莫干山麓的心安之地 等你来 慢慢生活',
  story:
    '麓禾村在莫干山麓，竹林与稻田之间。我们搭了木屋、辟了田地，想把日子过慢一点。白天农事手作，夜里篝火夜读，欢迎来小住。',
  facilities: [
    { name: '林间木屋', packId: 'stay', desc: '独栋木屋，带露台与夜读灯。' },
    { name: '营地早餐', packId: 'stay', desc: '柴火粥、现磨豆浆与当季果蔬。' },
    { name: '山泉戏水池', packId: 'day', desc: '引山泉水，夏日限定开放。' },
    { name: '儿童自然课堂', packId: 'day', desc: '认植物、做标本，半天一期。' },
    { name: '篝火广场', packId: 'night', desc: '入夜点篝火，配烤物与热饮。' },
    { name: '徒步小径', packId: null, desc: '环村两公里竹林步道，随时可走。' },
  ],
}

export const campPacks: CampPack[] = [
  {
    id: 'stay',
    name: '住宿套票',
    price: 588,
    unit: '/晚起',
    summary: '林间木屋过夜，含营地早餐。适合想把节奏放慢的一晚或两晚。',
    includes: ['林间木屋', '营地早餐'],
    notes: '入住 15:00 后，退房次日 11:00 前。不含本期需单独预约的营地活动。',
  },
  {
    id: 'day',
    name: '日间套票',
    price: 168,
    unit: '/人',
    summary: '白天使用营地设施：山泉戏水与儿童自然课堂，适合亲子半日游。',
    includes: ['山泉戏水池', '儿童自然课堂'],
    notes: '当日 9:00–16:00 有效。戏水池夏季开放，天气原因可能临时关闭。',
  },
  {
    id: 'night',
    name: '晚间套票',
    price: 98,
    unit: '/人',
    summary: '入夜篝火与烤物热饮，适合过夜客人加一场夜场。',
    includes: ['篝火广场'],
    notes: '约 19:00–21:30。儿童须家长陪同，勿靠近火堆。',
  },
]

export const bookingRules: RuleSection[] = [
  {
    heading: '预约须知',
    body: '预约成功后营地会尽快与你建联确认场次。请按所选日期与时段准时到达集合点，迟到可能无法补场。名额以当时余位为准。',
  },
  {
    heading: '退改规则',
    body: '活动开始 24 小时前可在「我的预约」中取消，取消后该条变为失效。24 小时内取消或未到场不退不改。改期请联系营地另行安排，视余位而定。',
  },
  {
    heading: '安全与陪同',
    body: '3–12 岁享儿童价，须家长全程陪同。水上、窑边等场景请遵守现场指引。如遇大雨或安全原因，营地将提前通知改期。',
  },
]

export const activities: Activity[] = [
  {
    id: 'a1',
    title: '挖甘蔗+榨汁+甘蔗棒棒糖',
    price: 68,
    childPrice: 38,
    notice: '3–12 岁享儿童价，需家长全程陪同；如遇小雨活动照常，大雨提前通知改期。',
    cover: activityCover,
    images: [activityCover, activityCoverPearl, kaodigua],
    intro:
      '走进甘蔗田亲手砍一节，现场榨汁，再做成一支甘蔗棒棒糖。适合亲子慢玩，约两小时。',
    tags: ['亲子', '农事体验', '甜品'],
    sessions: [
      {
        date: '2026-08-22',
        weekday: '周六',
        slots: [
          { time: '10:00–11:30', booked: 8, capacity: 8 },
          { time: '14:00–15:30', booked: 6, capacity: 8 },
          { time: '16:00–17:30', booked: 4, capacity: 8 },
        ],
      },
      {
        date: '2026-08-23',
        weekday: '周日',
        slots: [
          { time: '10:00–11:30', booked: 5, capacity: 8 },
          { time: '14:00–15:30', booked: 7, capacity: 8 },
          { time: '16:00–17:30', booked: 0, capacity: 8 },
        ],
      },
      {
        date: '2026-08-29',
        weekday: '周六',
        slots: [
          { time: '10:00–11:30', booked: 8, capacity: 8 },
          { time: '14:00–15:30', booked: 8, capacity: 8 },
          { time: '16:00–17:30', booked: 8, capacity: 8 },
        ],
      },
      {
        date: '2026-08-30',
        weekday: '周日',
        slots: [
          { time: '10:00–11:30', booked: 2, capacity: 8 },
          { time: '14:00–15:30', booked: 3, capacity: 8 },
          { time: '16:00–17:30', booked: 1, capacity: 8 },
        ],
      },
    ],
    highlights: ['下田砍一节甘蔗', '现榨一杯甘蔗汁', '熬糖做棒棒糖'],
    detail: [
      {
        heading: '活动流程',
        body: '集合后由农事老师带进甘蔗田，讲解怎么选节、怎么下刀。每人砍一节，现场削皮榨汁。最后到工坊把甘蔗汁熬成糖浆，倒进模具做棒棒糖，放凉后带走。',
      },
      {
        heading: '适合谁',
        body: '适合 4 岁以上亲子家庭，也欢迎想慢下来的大人。全程约两小时，节奏慢，不赶路。',
      },
      {
        heading: '费用包含',
        body: '包含农事体验、榨汁、棒棒糖材料与工具、保险。不含往返交通与正餐。',
      },
      {
        heading: '温馨提示',
        body: '请穿耐脏的长裤和包脚鞋，田里可能湿滑。如遇小雨照常进行，大雨会提前通知改期。',
      },
    ],
  },
  {
    id: 'a2',
    title: '划船捞河蚌+制作珍珠首饰',
    price: 128,
    childPrice: 88,
    notice: '3–12 岁享儿童价；水上活动儿童须穿救生衣并由家长同船陪同。',
    cover: activityCoverPearl,
    images: [activityCoverPearl, activityCover, kaodigua],
    intro:
      '清晨下河划船捞河蚌，开蚌取珠，把一颗珍珠做成手链或耳坠带回家。',
    tags: ['手作', '水上', '限定晨场'],
    sessions: [
      {
        date: '2026-08-24',
        weekday: '周一',
        slots: [
          { time: '06:30–08:00', booked: 8, capacity: 8 },
          { time: '08:30–10:00', booked: 8, capacity: 8 },
        ],
      },
      {
        date: '2026-08-25',
        weekday: '周二',
        slots: [
          { time: '06:30–08:00', booked: 8, capacity: 8 },
          { time: '08:30–10:00', booked: 8, capacity: 8 },
        ],
      },
      {
        date: '2026-08-31',
        weekday: '周一',
        slots: [
          { time: '06:30–08:00', booked: 8, capacity: 8 },
          { time: '08:30–10:00', booked: 8, capacity: 8 },
        ],
      },
    ],
    highlights: ['清晨划船下河', '开蚌取珍珠', '做一件首饰'],
    detail: [
      {
        heading: '活动流程',
        body: '天刚亮在码头集合，穿好救生衣后两人一船下河捞蚌。上岸后现场开蚌取珠，挑一颗喜欢的，由手作老师带着做成手链或耳坠。',
      },
      {
        heading: '适合谁',
        body: '适合喜欢手作和水上体验的人。会沾水，建议带一套换洗衣物。每场限 16 人。',
      },
      {
        heading: '费用包含',
        body: '包含船与救生衣、河蚌、珍珠、首饰材料与工具、保险。不含早餐。',
      },
      {
        heading: '温馨提示',
        body: '清晨水边较凉，请带一件外套。贵重物品尽量不带下水。',
      },
    ],
  },
  {
    id: 'a3',
    title: '挖地瓜+古法烤地瓜',
    price: 58,
    childPrice: 28,
    notice: '3–12 岁享儿童价；窑边温度高，请家长看好小朋友，勿靠近火口。',
    cover: kaodigua,
    images: [kaodigua, activityCover, activityCoverPearl],
    intro:
      '田间挖地瓜，用柴火窑慢慢烤熟。傍晚出窑，热乎乎分着吃。',
    tags: ['农事体验', '柴火', '傍晚场'],
    sessions: [
      {
        date: '2026-08-25',
        weekday: '周二',
        slots: [
          { time: '15:00–16:30', booked: 7, capacity: 10 },
          { time: '17:00–18:30', booked: 5, capacity: 10 },
        ],
      },
      {
        date: '2026-08-26',
        weekday: '周三',
        slots: [
          { time: '15:00–16:30', booked: 2, capacity: 10 },
          { time: '17:00–18:30', booked: 2, capacity: 10 },
        ],
      },
      {
        date: '2026-09-01',
        weekday: '周二',
        slots: [
          { time: '15:00–16:30', booked: 10, capacity: 10 },
          { time: '17:00–18:30', booked: 10, capacity: 10 },
        ],
      },
      {
        date: '2026-09-02',
        weekday: '周三',
        slots: [
          { time: '15:00–16:30', booked: 5, capacity: 10 },
          { time: '17:00–18:30', booked: 4, capacity: 10 },
        ],
      },
    ],
    highlights: ['田里挖地瓜', '柴火窑慢烤', '傍晚分着吃'],
    detail: [
      {
        heading: '活动流程',
        body: '下午在田边集合，跟着农事老师认藤、找薯、下锄。挖出的地瓜装进窑里，用柴火慢慢烤。傍晚出窑，大家围在一起分着吃。',
      },
      {
        heading: '适合谁',
        body: '适合亲子和想体验农事的人。挖地瓜要弯腰，建议穿方便活动的衣服。',
      },
      {
        heading: '费用包含',
        body: '包含农事体验、烤地瓜、茶水、保险。每人可带走一小袋生地瓜。',
      },
      {
        heading: '温馨提示',
        body: '窑边温度高，请看好小朋友。如遇雨天会改到棚下进行。',
      },
    ],
  },
]

export const getActivityById = (id: string) =>
  activities.find((item) => item.id === id)

export const getPackById = (id: string) =>
  campPacks.find((item) => item.id === id)

export const packLabel = (packId: string | null) =>
  packId ? (getPackById(packId)?.name ?? '套票') : '免费开放'

export const slotRemaining = (slot: ActivitySlot) => slot.capacity - slot.booked

export const isSlotFull = (slot: ActivitySlot) => slotRemaining(slot) <= 0

export const sessionBooked = (session: ActivitySession) =>
  session.slots.reduce((sum, slot) => sum + slot.booked, 0)

export const sessionCapacity = (session: ActivitySession) =>
  session.slots.reduce((sum, slot) => sum + slot.capacity, 0)

export const isSessionFull = (session: ActivitySession) =>
  session.slots.every(isSlotFull)

export const activityBooked = (activity: Activity) =>
  activity.sessions.reduce((sum, session) => sum + sessionBooked(session), 0)

export const activityCapacity = (activity: Activity) =>
  activity.sessions.reduce((sum, session) => sum + sessionCapacity(session), 0)

export const activityStatus = (activity: Activity): ActivityStatus =>
  activity.sessions.every(isSessionFull) ? 'full' : 'open'

export const nextOpenSession = (activity: Activity) =>
  activity.sessions.find((session) => !isSessionFull(session))
