import React from "react"
import { Card, CardHeader, CardText, CardBody, Button } from 'reactstrap'
import { Scatter } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  TimeScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'
import 'chartjs-adapter-date-fns'
import Plottable from "../../types/Plottable"
import './Plot.css'

ChartJS.register(
  CategoryScale,
  LinearScale,
  TimeScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
)

ChartJS.defaults.color = 'rgb(170,170,170)'

interface PlotProps {
  title: string,
  data: Plottable
  onSelect(): void
}

const colors = [
  '#5BC0DE',
  '#62C462',
  '#f89406'
]

const axisColor = '#666'

const axisDefault = {
  grid: {
    color: axisColor,
    drawBorder: false,
  },
  ticks: {
    color: axisColor
  },
  title: {
    color: '#fff'
  }
}

const Plot = (props: PlotProps) => {
  return (
    <Card className='Plot'>
      <CardHeader>
        <div className='Plot-name'>{props.title}</div>
        <Button onClick={() => props.onSelect()} size='sm' className='float-end'>Detail</Button>
      </CardHeader>
      <CardBody>
        <CardText>
          <Scatter 
            data={{
              labels: props.data.dates,
              datasets: props.data.data.map((d, i) => {
                return {
                  ...d,
                  tension: 0.5,
                  pointRadius: 0,
                  showLine: true,
                  backgroundColor: colors[i % colors.length],
                  borderColor: colors[i % colors.length],
                  spanGaps: false,
                }
              })
            }}
            options={{
              responsive: true,
              scales: {
                x: {
                  ...axisDefault,
                  type: 'time',
                },
                y: {
                  ...axisDefault,
                  type: 'linear',
                }
              }
            }}
          />
        </CardText>
      </CardBody>
    </Card>
  )
}

export default Plot
