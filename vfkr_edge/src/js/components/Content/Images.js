import React from "react";

import {Card, Col, Row} from "react-materialize";

import Image from "./Image";

export default class Images extends React.Component {
  constructor(props) {
	  super(props);
	  this.state = {
	    names: []
	  };

    this.update()
  }

  update() {
    $.get("http://localhost:5000/v2/_catalog", function(data, status){
        if (status == 'success') {
          this.setState({names: data['repositories']});
        }
    }.bind(this));

    setTimeout(this.update.bind(this), 1000);
  }

  render() {
  	const names = this.state.names

    return (
      <div style={{
            display: "flex",
            flexWrap: "wrap",
            flexFlow: "row wrap"
          }}> 
        {
          names.map((name) => 
          <div key={name} style={{
            flex: 1
          }}>
            <Image name={name} />
          </div>)}
      </div>
    )
  }
}
