
export const formatDate = (d: Date): string => `${d.getFullYear()}-${padZeros(d.getMonth() + 1)}-${padZeros(d.getDate())}`

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

const padZeros = (v: number): string => {
  if (v < 10) {
    return `0${v}`
  }
  return `${v}`
}