import React from "react";

import {
  Navbar,
  NavItem,
  Icon
} from "react-materialize";

import Title from "./Header/Title";

export default class Header extends React.Component {
  render() {
    return ( < div style = {
        {
          height: "65px"
        }
      } >
      < Title / >
      < Navbar brand = "Edge Controller"
      right style = {
        {
          background: 'rgb(37, 37, 37)'
        }
      } >
      < NavItem href = 'get-started.html' >
      < Icon className = 'search-icon'
      style = {
        {
          marginTop: "17 !important"
        }
      } > search < /Icon> < /NavItem> < /Navbar> < /div>
    );
  }
}
