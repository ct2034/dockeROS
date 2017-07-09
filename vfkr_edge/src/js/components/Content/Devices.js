import React from "react";

import {Card, Col, Row} from "react-materialize";

import Device from "./Device";

export default class Devices extends React.Component {
  constructor(props) {
	  super(props);
	  this.state = {
	    ids: props.ids
	  };
	}

  render() {
  	const ids = this.props.ids

    return (
      <div style={{
            display: "flex",
            flexWrap: "wrap",
            flexFlow: "row wrap",
            alignItems: "flex-start"
          }}> 
        {
          ids.map((id) => 
          <div id={id} style={{
            flex: 1
          }}>
            <Device id={id} key={id} />
          </div>)}
      </div>
    )
  }
}
