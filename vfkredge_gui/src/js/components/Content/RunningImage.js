import React from "react";

import {
	Button,
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
				< p key = "delte" center > <div>
					<Button small center floating class='black' icon='clear'
					style = {{
						padding: 0,
						height: 38
					}}
					onClick={function() {
					  Materialize.toast('Stopping ' + this.props.name, 4000);
						$.ajax({
							type: "POST",
							url: "http://"+this.props.host+":2375/containers"+this.props.name+"/kill",
							data: JSON.stringify({}),
							success: function(data, status) {
								console.log("KILL");
								console.log(status);
								console.log(data);
								$.ajax({
									type: "DELETE",
									url: "http://"+this.props.host+":2375/containers"+this.props.name,
									data: JSON.stringify({}),
									success: function(data, status) {
										console.log("DELETE");
										console.log(status);
										console.log(data);
									}.bind(this),
								  error: function(e) {
										console.log("DELETE error");
								    console.log(e);
								  }.bind(this)
								});
							}.bind(this),
						  error: function(e) {
								console.log("KILL error");
						    console.log(e);
						  }.bind(this)
						});
					}.bind(this)} />
				</div>	< /p >
			</div>
		);

	}
}
