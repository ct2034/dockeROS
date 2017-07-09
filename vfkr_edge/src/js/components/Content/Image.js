import React from "react";

import {Card, Col} from "react-materialize";
import PropTypes from 'prop-types';
import { DragSource } from 'react-dnd';

export default class Image extends React.Component {
  render() {
    return (
		<Card className='blue-grey darken-1' textClassName='white-text'>
			<p><b>ID</b>: {this.props.id}</p> 
			<p><b>Name</b>: Image {this.props.id}</p> 
			<p><b>Tag</b>: whatever{this.props.id}</p> 
		</Card>
    );
  }
}
