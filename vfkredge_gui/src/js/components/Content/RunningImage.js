import React from "react";

import {
	Card,
	Col
} from "react-materialize";

export default class RunningImage extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		return ( 
			<div>
				< p key = "name" > < b >Name< /b>: {this.props.name} < /p > 
				< p key = "image" > < b >Image< /b>: {this.props.image} < /p >  
				< p key = "command" > < b >Command< /b>: {this.props.command} < /p >
				< p key = "status" > < b >Status< /b>: {this.props.status} < /p >
			</div>
		);

	}
}
