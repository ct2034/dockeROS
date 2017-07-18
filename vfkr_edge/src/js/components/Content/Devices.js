import React from "react";

import {Card, Col, Row} from "react-materialize";

import Device from "./Device";

export default class Devices extends React.Component {
  constructor(props) {
	  super(props);
	  this.state = {
	    ids: ["localhost:2375", "cchsim.ipa.stuttgart:2375"]
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
