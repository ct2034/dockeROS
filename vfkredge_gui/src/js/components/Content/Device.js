import React from "react";

import {
	Button,
	Card,
	Col,
	Collapsible,
	CollapsibleItem
} from "react-materialize";
import PropTypes from 'prop-types';
import { DragSource } from 'react-dnd';
import {EventEmitter} from 'fbemitter';

import Bar from "./Bar";
import RunningImage from "./RunningImage";


const deviceTarget = {
	drop(props) {
		console.log(props)
	}
};


function collect(connect, monitor) {
	return {
		connectDropTarget: connect.dropTarget(),
		isOver: monitor.isOver()
	};
}

export default class Device extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
  		metrics_cpu: 0,
	    metrics_mem: 0,
		deployable: false,
		to_deploy: "",
		running_images: []
  	};

  	this.updateMetrics()
	this.props.emitter.addListener('deploy', (name) => {
		console.log(name);
		this.setState({
			deployable: true,
			to_deploy: name
		})
	});
	this.props.emitter.addListener('deployed_to', (name) => {
		// console.log(name);
		this.setState({deployable: false})
	});
  }

  updateMetrics() {
	$.get("http://"+this.props.host+":5005/rob_metrics", function(data, status) {
		if (status == 'success') {
			this.setState({
		  		metrics_cpu: data.cpu_usg,
				metrics_mem: data.ram_usg
		  	})
			//console.log(data);
		} else {
		  	this.setState({
		  		metrics_cpu: Math.random() * 4 - 2 + this.base_metrics_cpu,
				metrics_mem: Math.random() * 2 - 1 + this.base_metrics_mem
		  	})
		}
	}.bind(this));
	$.get("http://"+this.props.host+":2375/containers/json", function(data, status) {
		if (status == 'success') {
			this.setState({
				running_images: data
			});
			console.log("running_images")
			console.log(data);
		} else {
		  	this.setState({
		  		running_images: ['laser_node']
		  	})
		}
	}.bind(this));

  	setTimeout(this.updateMetrics.bind(this), 1000);
  }

  render() {
    return (
		<Card className='cyan darken-2' textClassName='white-text' style={{
			minWidth: 200,
			maxWidth: 300,
			margin: "5px"
		}}>
			<Bar val={this.state.metrics_cpu} name="CPU" id="1" />
			<Bar val={this.state.metrics_mem} name="Memory" id="2" />
			<p><b>Name</b>: {this.props.name}</p>
			<p><b>Host</b>: {this.props.host}</p>

			{(this.props.name == "lidar") ? (
				<Collapsible>
					<CollapsibleItem header="lidar" key="lidar"
							icon='play_circle_filled'>
							<RunningImage name="lidar"
							image="/sick_lidar"
							command="/run.sh"
							status="up"
							host='localhost' />
						</CollapsibleItem>
				</Collapsible>
			) : (
				(this.state.running_images.length == 0) ? (<p><i>No images (yet)</i></p>) : (
					<Collapsible>
						{this.state.running_images.map((image) =>
							(<CollapsibleItem header={image["Names"][0]} key={image["Names"][0]}
								icon={(image["State"] == "running") ? 'play_circle_filled' : 'pause_circle_filled'}>
								<RunningImage name={image["Names"][0]}
								image={image["Image"]}
								command={image["Command"]}
								status={image["Status"]}
								host={this.props.host} />
							</CollapsibleItem>)
							)}
					</Collapsible>
				)
			)}
			<Button floating className="black" icon='fast_forward' disabled={
				(this.state.deployable) ? (false) : (true)
			} onClick={function() {
				this.props.emitter.emit('deployed_to', this.props.id);
				Materialize.toast('Deploying ' + this.state.to_deploy + ' to ' + this.props.name, 4000);
				$.ajax({
					type: "POST",
					url: "http://"+this.props.id+":2375/containers/create?name="+this.state.to_deploy,
					data: JSON.stringify({
						"Image": "space:5000/"+this.state.to_deploy
					}),
					success: function(data, status) {
						console.log("DEPLOY");
						console.log(status);
						console.log(data);
						$.ajax({
							type: "POST",
							url: "http://"+this.props.id+":2375/containers/"+this.state.to_deploy+"/start",
							data: JSON.stringify({}),
							success: function(data, status) {
								console.log("START");
								console.log(status);
								console.log(data);
							}.bind(this),
						  error: function(e) {
								console.log("START");
						    console.log(e);
						  }.bind(this)
						});
					}.bind(this),
				  error: function(e) {
						console.log("DEPLOY");
				    console.log(e)
				  }.bind(this),
					dataType: "json",
  				contentType: "application/json"
				});
			}.bind(this)}
			style={{
			    position: "absolute",
			    left: 1,
			    bottom: "-6",
			    height: "38px",
			    padding: 0
			}} />
		</Card>
    );
  }
}
