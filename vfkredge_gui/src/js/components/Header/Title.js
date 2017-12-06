import React from "react";


export default class Title extends React.Component {
  constructor() {
  	super();
  	this.state = {title: "Edge Controller"};
  }

  render() {
    return (
	  <title>
	  	{this.state.title}
	  </title>
    );
  }
}
