import WeatherItemResponse from "./WeatherItemResponse"

export default class WeatherItem {
  timestamp: Date
  avgWindSpeed: number
  minWindSpeed: number
  maxWindSpeed: number
  temperature: number
  gas: number
  relativeHumidity: number
  pressure: number

  constructor(r: WeatherItemResponse) {
    this.timestamp = new Date(Date.parse(r.timestamp))
    this.avgWindSpeed = r.avg_wind_speed
    this.minWindSpeed = r.min_wind_speed
    this.maxWindSpeed = r.max_wind_speed
    this.temperature = r.temperature
    this.gas = r.gas
    this.relativeHumidity = r.relative_humidity
    this.pressure = r.pressure
  }
}
