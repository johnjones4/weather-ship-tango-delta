import React from "react"
import DatePicker from '../DatePicker/DatePicker'
import { Navbar, Button, NavbarBrand, Nav, NavItem, Form, FormGroup, Label, Input } from 'reactstrap'
import './Header.css'

interface HeaderProps {
  showBack: boolean
  backSelected(): void
  start: Date
  end: Date
  datesChange(start: Date, end: Date): void
}

const Header = (props: HeaderProps) => {
  return (
    <Navbar
      color='dark'
      expand="md"
      dark
      className='Header'
    >
      <NavbarBrand>
        Weather
      </NavbarBrand>
      <Nav
        className="me-auto"
        navbar
      >
        { props.showBack && (
          <NavItem>
            <Button color='dark' onClick={() => props.backSelected()}>Back</Button>
          </NavItem>
        ) }
      </Nav>
      <div className='Header-form'>
        <DatePicker date={props.start} dateChanged={d => props.datesChange(d, props.end)} />
        <DatePicker date={props.end} dateChanged={d => props.datesChange(props.start, d)} />
      </div>
    </Navbar>
  )
}

export default Header
