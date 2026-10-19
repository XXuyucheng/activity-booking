export const formatRange = (start: string, end: string) => {
  const from = new Date(start)
  const to = new Date(end)
  const date = from.toLocaleDateString('zh-CN', {
    month: 'numeric',
    day: 'numeric',
    weekday: 'short',
  })
  const hm = (value: Date) =>
    value.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  return `${date} ${hm(from)}–${hm(to)}`
}

export const formatDateTime = (value: string) =>
  new Date(value).toLocaleString('zh-CN', {
    month: 'numeric',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })

const shanghaiDay = new Intl.DateTimeFormat('en-CA', {
  timeZone: 'Asia/Shanghai',
  year: 'numeric',
  month: '2-digit',
  day: '2-digit',
})

export const shanghaiDateKey = (value: string | Date) =>
  shanghaiDay.format(typeof value === 'string' ? new Date(value) : value)

export const todayShanghaiKey = () => shanghaiDateKey(new Date())
