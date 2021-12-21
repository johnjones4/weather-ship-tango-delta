
export const formatDate = (d: Date): string => `${d.getFullYear()}-${d.getMonth() + 1}-${d.getDate()}`

export const parseDate = (ds: string, hour: number, minute: number): Date => {
  const parts = ds.split('-').map(s => parseInt(s))
  if (parts.length !== 3) {
    return new Date()
  }
  return new Date(parts[0], parts[1] - 1, parts[2], hour, minute, 0)
}

export const updateDateHour = (d: Date, h: number): Date => {
  return new Date(d.getFullYear(), d.getMonth(), d.getDate(), h, d.getMinutes(), d.getSeconds())
}

export const updateDateMinute = (d: Date, m: number): Date => {
  return new Date(d.getFullYear(), d.getMonth(), d.getDate(), d.getHours(), m, d.getSeconds())
}
