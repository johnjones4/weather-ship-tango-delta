import React from "react"
import { Input } from 'reactstrap'
import { formatDate, parseDate, updateDateHour, updateDateMinute } from "../../util"
import './DatePicker.css'

interface DatePickerProps {
  date: Date
  dateChanged(d: Date): void
}

const DatePicker = (props: DatePickerProps) => {
  return (
    <div className='DatePicker'>
      <Input
        name='start-date'
        type='date'
        value={formatDate(props.date)}
        onChange={(e) => props.dateChanged(parseDate(e.target.value, props.date.getHours(), props.date.getMinutes()))}
      />
      <Input 
        name='start-hour'
        type='select'
        onChange={(e) => props.dateChanged(updateDateHour(props.date, parseInt(e.target.value)))}
        value={props.date.getHours()}
        >
          { Array.from(Array(23).keys()).map(i => (<option key={i} value={i + 1}>{i + 1}</option>)) }
      </Input>
      <Input 
        name='start-minute'
        type='select'
        onChange={(e) => props.dateChanged(updateDateMinute(props.date, parseInt(e.target.value)))}
        value={props.date.getMinutes()}
        >
          { Array.from(Array(60).keys()).map(i => (<option key={i} value={i + 1}>{i + 1}</option>)) }
      </Input>
    </div>
  )
}

export default DatePicker
