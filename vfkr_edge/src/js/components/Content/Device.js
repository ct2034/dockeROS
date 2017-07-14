import React from "react";

import {Card, Col, Collapsible, CollapsibleItem} from "react-materialize";
import PropTypes from 'prop-types';
import { DragSource } from 'react-dnd';

import Bar from "./Bar";
import Image from "./Image";


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

// @DropTarget('image', deviceTarget, collect)
export default class Device extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
  		metrics: {
  			cpu: 32,
	        mem: 82
	    }
  	};
  }

  render() {
    return (
		<Card className='cyan darken-2' textClassName='white-text' style={{
			minWidth: 200,
			maxWidth: 300,
			margin: "5px"
		}}>
			<Bar val="50" name="CPU" />
			<Bar val="98" name="Memory" />
			<p><b>ID</b>: {this.props.id}</p> 
			<p><b>Name</b>: Device {this.props.id}</p> 
			<Collapsible>
				<CollapsibleItem header='First' icon='pause_circle_filled'>
					<Image id="3" />
				</CollapsibleItem>
				<CollapsibleItem header='Second' icon='play_circle_filled'>
					<p>Lorem ipsum dolor sit amet</p>
				</CollapsibleItem>
			</Collapsible>
		</Card>
    );
  }
}
