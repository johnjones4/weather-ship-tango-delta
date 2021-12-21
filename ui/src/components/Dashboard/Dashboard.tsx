import { Component } from "react";
import { Weather } from "../../types/Weather"
import WeatherFeature from "../../types/WeatherFeature";
import Plot from "../Plot/Plot";
import { Container } from 'reactstrap'
import './Dashboard.css'
import Header from "../Header/Header";

interface DashboardProps {

}

interface DashboardState {
  weather?: Weather
  start: Date,
  end: Date
  focusedPlot: number | null
  loading: boolean
}

export default class Dashboard extends Component<DashboardProps,DashboardState> {
  constructor(props: DashboardProps) {
    super(props)
    this.state = {
      start: new Date(new Date().getTime() - 1000 * 60 * 60 * 24),
      end: new Date(),
      focusedPlot: null,
      loading: false
    }
  }

  async componentDidMount() {
    this.setState({
      loading: true
    })
    const weather = await Weather.load(this.state.start, this.state.end)
    this.setState({
      weather,
      loading: false
    })
  }

  async updateDateRange(start: Date, end: Date) {
    this.setState({
      loading: true,
      start,
      end,
    })
    const weather = await Weather.load(start, end)
    this.setState({
      weather,
      loading: false
    })
  }

  render() {
    if (!this.state.weather || !this.state.weather.hasData()) {
      return null
    }

    const plots = [
      {
        title: `Wind Speed (${this.state.weather.getCurrentFeatureDescription(WeatherFeature.avgWindSpeed)})`,
        data: this.state.weather.getPlottable([WeatherFeature.avgWindSpeed, WeatherFeature.minWindSpeed, WeatherFeature.maxWindSpeed])
      },
      {
        title: `Pressure (${this.state.weather.getCurrentFeatureDescription(WeatherFeature.pressure)})`,
        data: this.state.weather.getPlottable([WeatherFeature.pressure])
      },
      {
        title: `Relative Humidity (${this.state.weather.getCurrentFeatureDescription(WeatherFeature.relativeHumidity)})`,
        data: this.state.weather.getPlottable([WeatherFeature.relativeHumidity])
      },
      {
        title: `Temperature (${this.state.weather.getCurrentFeatureDescription(WeatherFeature.temperature)})`,
        data: this.state.weather.getPlottable([WeatherFeature.temperature])
      }
    ].map((p, i) => {
      return (
        <Plot
          key={i}
          onSelect={() => this.setState({focusedPlot: i})}
          title={p.title}
          data={p.data}
        /> 
      )
    })
    return (
      <Container fluid className='Dashboard'>
        <Header
          showBack={this.state.focusedPlot !== null}
          backSelected={() => this.setState({focusedPlot: null})}
          start={this.state.start}
          end={this.state.end}
          datesChange={(start: Date, end: Date) => this.updateDateRange(start, end)}
        />
        { this.state.focusedPlot !== null ? plots[this.state.focusedPlot] : (<div className='Dashboard-grid'>{plots}</div>) }
        { this.state.loading && (<div className='Dashboard-loading'>Loading ...</div>) }
      </Container>
    )
  }
}
