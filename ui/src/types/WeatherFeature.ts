enum WeatherFeature {
  avgWindSpeed,
  minWindSpeed,
  maxWindSpeed,
  temperature,
  gas,
  relativeHumidity,
  pressure,
}

export const weatherFeatureString = (key: WeatherFeature) => {
  switch (key) {
    case WeatherFeature.avgWindSpeed:
      return 'Average Wind Speed'
    case WeatherFeature.minWindSpeed:
      return 'Min Wind Speed'
    case WeatherFeature.maxWindSpeed:
      return 'Max Wind Speed'
    case WeatherFeature.temperature:
      return 'Temperature'
    case WeatherFeature.gas:
      return 'Gas'
    case WeatherFeature.relativeHumidity:
      return 'Relative Humidity'
    case WeatherFeature.pressure:
      return 'Pressure'
  }
}

export default WeatherFeature