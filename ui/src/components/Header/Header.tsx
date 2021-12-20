import React from "react"
import { Navbar, Button, NavbarBrand, Nav, NavItem } from 'reactstrap'
import './Header.css'

interface HeaderProps {
  showBack: boolean
  backSelected(): void
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
    </Navbar>
  )
}

export default Header