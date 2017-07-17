import React from "react";

import {Card, Col, Row} from "react-materialize";

import Device from "./Device";

export default class Devices extends React.Component {
  constructor(props) {
	  super(props);
	  this.state = {
	    ids: [0, 1]
	  };
	}

  render() {
  	const ids = this.state.ids

    return (
      <div style={{
            display: "flex",
            flexWrap: "wrap",
            flexFlow: "row wrap",
            alignItems: "flex-start"
          }}> 
        {
          ids.map((id) => 
          <div key={id} style={{
            flex: 1
          }}>
            <Device id={id} />
          </div>)}
      </div>
    )
  }
}
