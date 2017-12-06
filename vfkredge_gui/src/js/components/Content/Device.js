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
  	this.base_metrics_cpu = Math.random() * 20 + 15
  	this.base_metrics_mem = Math.random() * 30 + 40
    this.state = {
  		metrics_cpu: this.base_metrics_cpu,
	    metrics_mem: this.base_metrics_mem,
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
	$.get("http://"+this.props.id+":5005/rob_metrics", function(data, status) {
		if (status == 'success') {
			this.setState({
		  		metrics_cpu: data.cpu_usg,
				metrics_mem: data.ram_usg
		  	})
			// console.log(data);
		} else {
		  	this.setState({
		  		metrics_cpu: Math.random() * 4 - 2 + this.base_metrics_cpu,
				metrics_mem: Math.random() * 2 - 1 + this.base_metrics_mem
		  	})
		}
	}.bind(this));
	$.get("http://"+this.props.id+":2375/containers/json", function(data, status) {
		if (status == 'success') {
			this.setState({
				running_images: data
			});
			// console.log(data);
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
			<p><b>Name</b>: {this.props.id.split(':')[0].toUpperCase()}</p> 
			<p><b>Host</b>: {this.props.id}</p> 
			{(this.state.running_images.length == 0) ? (<p><i>No images (jet)</i></p>) : (
				<Collapsible>
					{this.state.running_images.map((image) =>
						(<CollapsibleItem header={image["Names"][0]} key={image["Names"][0]} 
							icon={(image["State"] == "running") ? 'play_circle_filled' : 'pause_circle_filled'}>
							<RunningImage name={image["Names"][0]} 
							image={image["Image"]} 
							command={image["Command"]}
							status={image["Status"]} />
						</CollapsibleItem>)
						)}	
				</Collapsible>
			)}
			<Button floating className="black" icon='fast_forward' disabled={
				(this.state.deployable) ? (false) : (true)
			} onClick={function() {
				this.props.emitter.emit('deployed_to', this.props.id);
				Materialize.toast('Deploying ' + this.state.to_deploy + ' to ' + this.props.id, 4000);
				new_running_images = this.state.running_images.slice()
				new_running_images.push(
						{
					        "Names": [
					            "/"+this.state.to_deploy
					        ],
					        "Image": this.state.to_deploy,
					        "Command": "/delpoyed.sh",
					        "State": "running",
					        "Status": "Up now"
				    	}	
				    )
				this.setState({
					deployable: false,
					to_deploy: '',
					running_images: new_running_images
				})
				// $.post( "http://"+
				// 		this.props.id+
				// 		"/images/create?fromImage="+
				// 		this.state.to_deploy+
				// 		"&repo=cchpc.ipa.stuttgart:5000"	, 
				// function(data, status) {
				// 	console.log("DEPLOY");
				// 	console.log(status);
				// 	console.log(data);
				// }.bind(this));
				// $.post( "http://"+this.props.id+"/containers/create", 
				// { 
				// 	"Image": "cchpc.ipa.stuttgart:5000/"+this.state.to_deploy 
				// }, function(data, status) {
				// 	console.log("DEPLOY");
				// 	console.log(status);
				// 	console.log(data);
				// }.bind(this));
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
