import React from "react";

import {Navbar, NavItem, Icon} from "react-materialize";

import Title from "./Header/Title";

export default class Header extends React.Component {
  render() {
    return (
      <div>
        <Title/>
        <Navbar brand="Edge Controller" className='grey darken-3' right>
          <NavItem href='get-started.html'><Icon>search</Icon></NavItem>
        </Navbar>
      </div>
    );
  }
}
