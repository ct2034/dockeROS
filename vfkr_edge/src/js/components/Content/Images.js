import React from "react";

import {Card, Col, Row} from "react-materialize";

import Image from "./Image";

export default class Images extends React.Component {
  constructor(props) {
	  super(props);
	  this.state = {
	    ids: props.ids
	  };
	}

  render() {
  	const ids = this.props.ids
    var ids_l = []
    var ids_r = []
    for (var i = 0; i < ids.length; i = i+1) {
        if (i < ids.length / 2) {  
          ids_l.push(ids[i]);
        } else {
          ids_r.push(ids[i]);
        }
    }; 

    return (
      <Row style={{
            display: "flex",
            flexDirection: "row"
          }}>
        <Col style={{
            flex: 1
          }}> 
        {// left
          ids_l.map((id) => 
          <Image id={id} key={id} />)}
        </Col>
        <Col style={{
            flex: 1
          }}> 
        {// right
          ids_r.map((id) => 
          <Image id={id} key={id} />)}
        </Col>
    	</Row>
    )
  }
}
