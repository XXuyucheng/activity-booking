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
