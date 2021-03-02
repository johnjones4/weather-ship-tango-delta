const DIRECTION = {
  NONE: 'none',
  UP: 'up',
  DOWN: 'down'
}

const TEMP_COLORS = [
  {
    value: 0,
    hexes: [
      0xFF,
      0xFF,
      0xF9
    ]
  },
  {
    value: 20,
    hexes: [
      0x47,
      0x98,
      0xF9
    ]
  },
  {
    value: 40,
    hexes: [
      0x09,
      0x7A,
      0xD3
    ]
  },
  {
    value: 75,
    hexes: [
      0xF9,
      0xAE,
      0x47
    ]
  },
  {
    value: 100,
    hexes: [
      0xF9,
      0x5F,
      0x47
    ]
  },
]

const temperatureDiv = document.getElementById('temperature')
const windSpeedDiv = document.getElementById('wind-speed')
const relativeHumidityDiv = document.getElementById('relative-humidity')
const pressureDiv = document.getElementById('pressure')

const loadWeather = async () => {
  const resp = await fetch('/api/weather/average?range=10')
  return await resp.json()
}

const getDirection = (oldValue, newValue) => {
  if (newValue > oldValue) {
    return DIRECTION.UP
  } else if (newValue < oldValue) {
    return DIRECTION.DOWN
  } else {
    return DIRECTION.NONE
  }
}

const doConversion = (key, value) => {
  switch (key) {
    case 'avg_wind_speed':
    case 'min_wind_speed':
    case 'max_wind_speed':
      return value * 2.237
    case 'temperature':
      return value * 1.8 + 32
    case 'pressure':
      return value / 3386
    default:
      return value
  }
}

const prepareWeatherData = (weather) => {
  const outcome = {}
  for (const key in weather) {
    outcome[key] = {
      value: doConversion(key, weather[key].current_value),
      direction: getDirection(weather[key].previous_value, weather[key].current_value)
    }
  }
  return outcome
}

const generateClasses = (item) => ['value', `trend-${item.direction}`].join(' ')

const joinHexes = (hexes) => '#' + hexes.map(h => {
  const hex = h.toString(16)
  if (hex.length === 1) {
    return `0${hex}`
  }
  return hex
}).join('')

const generateColor = (value, colors) => {
  if (value <= colors[0].value) {
    return joinHexes(colors[0].hexes)
  }
  let lastColor = colors[0]
  for (const color of colors) {
    if (value <= color.value) {
      const pcnt = (value - lastColor.value) / (color.value - lastColor.value)
      const hexes = color.hexes.map((h, i) => lastColor.hexes[i] + parseInt(pcnt * (h - lastColor.hexes[i])))
      return joinHexes(hexes)
    } else {
      lastColor = color
    }
  }
  return joinHexes(lastColor.hexes)
}

const renderData = (weather) => {
  document.body.style.background = `linear-gradient(0deg, ${generateColor(weather.temperature.value - 5, TEMP_COLORS)} 0%, ${generateColor(weather.temperature.value + 5, TEMP_COLORS)} 100%)`

  temperatureDiv.innerHTML = `${weather.temperature.value.toFixed(1)}&deg;`
  temperatureDiv.classList = generateClasses(weather.temperature)

  windSpeedDiv.innerHTML = weather.avg_wind_speed.value.toFixed(1)
  windSpeedDiv.classList = generateClasses(weather.avg_wind_speed)

  relativeHumidityDiv.innerHTML = `${weather.relative_humidity.value.toFixed(0)}%`
  relativeHumidityDiv.classList = generateClasses(weather.relative_humidity)

  pressureDiv.innerHTML = weather.pressure.value.toFixed(2)
  pressureDiv.classList = generateClasses(weather.pressure)
}

const update = async () => {
  const weather = await loadWeather()
  const preparedWeather = prepareWeatherData(weather)
  renderData(preparedWeather)
}

setInterval(update, 60000)
update()
