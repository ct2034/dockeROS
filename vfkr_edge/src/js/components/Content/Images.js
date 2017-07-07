import React from "react";

import {Card, Col} from "react-materialize";

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
    return (<div>
    	{ids.map((id) => 
    		<Image id={id} key={id} />)}
    	</div>
    )
  }
}
