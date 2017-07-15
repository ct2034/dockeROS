import React from "react";

import {Card, Col, Row} from "react-materialize";

import Image from "./Image";

export default class Images extends React.Component {
  constructor(props) {
	  super(props);
	  this.state = {
	    ids: props.ids
	  };

    $.get("http://localhost:5000/v2/_catalog", function(data, status){
        console.log(data);
    });
  }


  render() {
  	const ids = this.props.ids

    return (
      <div style={{
            display: "flex",
            flexWrap: "wrap",
            flexFlow: "row wrap"
          }}> 
        {
          ids.map((id) => 
          <div key={id} style={{
            flex: 1
          }}>
            <Image id={id} />
          </div>)}
      </div>
    )
  }
}
