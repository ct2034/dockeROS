import React from "react";

import {Card, Col, Collapsible, CollapsibleItem} from "react-materialize";
import PropTypes from 'prop-types';
import { DragSource } from 'react-dnd';

import Bar from "./Bar";

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
			maxWidth: 250,
			margin: "5px"
		}}>
			<Bar val="50" name="CPU" />
			<Bar val="98" name="Memory" />
			<p><b>ID</b>: {this.props.id}</p> 
			<p><b>Name</b>: Device {this.props.id}</p> 
			<Collapsible>
				<CollapsibleItem header='First' icon='filter_drama'>
					<p>Lorem ipsum dolor sit amet</p>
				</CollapsibleItem>
				<CollapsibleItem header='Second' icon='place'>
					<p>Lorem ipsum dolor sit amet</p>
				</CollapsibleItem>
			</Collapsible>
		</Card>
    );
  }
}
