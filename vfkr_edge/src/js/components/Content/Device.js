import React from "react";

import {Card, Col, Collapsible, CollapsibleItem} from "react-materialize";
import PropTypes from 'prop-types';
import { DragSource } from 'react-dnd';

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
		running_images: []
  	};

  	this.updateMetrics()
  }

  updateMetrics() {
  	this.setState({
  		metrics_cpu: Math.random() * 4 - 2 + this.base_metrics_cpu,
		metrics_mem: Math.random() * 2 - 1 + this.base_metrics_mem
  	})
	$.get("http://"+this.props.id+"/containers/json", function(data, status) {
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
			<p><b>Host</b>: {this.props.id}</p> 
			<p><b>Name</b>: Device {this.props.id}</p> 
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
		</Card>
    );
  }
}
