import Plottable from './Plottable'
import WeatherFeature, { weatherFeatureString } from './WeatherFeature'
import WeatherItem from './WeatherItem'
import WeatherItemResponse from './WeatherItemResponse'


export class Weather {
  private items: WeatherItem[]

  constructor(items: WeatherItem[]) {
    this.items = items
  }

  hasData() {
    return this.items.length > 0
  }

  getCurrentFeatureDescription(key: WeatherFeature): string {
    if (!this.hasData()) {
      return ''
    }
    const lastItem = this.items[this.items.length - 1]
    switch (key) {
      case WeatherFeature.avgWindSpeed:
        return `${lastItem.avgWindSpeed.toFixed(2)} m/s`
      case WeatherFeature.minWindSpeed:
        return `${lastItem.minWindSpeed.toFixed(2)} m/s`
      case WeatherFeature.maxWindSpeed:
        return `${lastItem.maxWindSpeed.toFixed(2)} m/s`
      case WeatherFeature.temperature:
        return `${lastItem.temperature.toFixed(2)} C`
      case WeatherFeature.gas:
        return `${lastItem.gas.toFixed(2)}`
      case WeatherFeature.relativeHumidity:
        return `${lastItem.relativeHumidity.toFixed(2)}%`
      case WeatherFeature.pressure:
        return `${lastItem.pressure.toFixed(2)} mbar`
      default:
        return ''
    }
  }

  getPlottable(keys: WeatherFeature[]): Plottable {
    return {
      dates: this.items.map(i => i.timestamp),
      data: keys.map(key => {
        return {
          label: weatherFeatureString(key),
          data: this.items.map(w => {
            switch (key) {
              case WeatherFeature.avgWindSpeed:
                return w.avgWindSpeed
              case WeatherFeature.minWindSpeed:
                return w.minWindSpeed
              case WeatherFeature.maxWindSpeed:
                return w.maxWindSpeed
              case WeatherFeature.temperature:
                return w.temperature
              case WeatherFeature.gas:
                return w.gas
              case WeatherFeature.relativeHumidity:
                return w.relativeHumidity
              case WeatherFeature.pressure:
                return w.pressure
              default:
                return 0
            }
          })
        }
      })
    }
  }

  static async load(start: Date, end: Date): Promise<Weather> {
    const params = new URLSearchParams([
      ['start', `${Math.floor(start.getTime() / 1000)}`],
      ['end', `${Math.ceil(end.getTime() / 1000)}`]
    ])
    const response = await fetch('/api/weather?' + params.toString())
    const items = await response.json() as WeatherItemResponse[]
    return new Weather(items.map(w => new WeatherItem(w)))
  }
}
