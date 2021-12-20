export default interface WeatherItemResponse {
  timestamp: string
  avg_wind_speed: number
  min_wind_speed: number
  max_wind_speed: number
  temperature: number
  gas: number
  relative_humidity: number
  pressure: number
}