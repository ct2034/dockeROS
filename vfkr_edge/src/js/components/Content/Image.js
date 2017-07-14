import React from "react";

import {
	Card,
	Col
} from "react-materialize";
import PropTypes from 'prop-types';
import {
	DragSource
} from 'react-dnd';

const imageSource = {
	beginDrag(props) {
		return {
			imageId: props.id
		};
	}
};

function collect(connect, monitor) {
	return {
		connectDragSource: connect.dragSource(),
		isDragging: monitor.isDragging()
	}
}

@DragSource('image', imageSource, collect)
export default class Image extends React.Component {
	static propTypes = {
		connectDragSource: PropTypes.func.isRequired,
		isDragging: PropTypes.bool.isRequired
	};

	render() {
		const {
			id,
			connectDragSource,
			isDragging
		} = this.props;

		// console.log(this.props)

		return connectDragSource( < div style = {
				{
					opacity: isDragging ? 0.5 : 1
				}
			} >
			< Card textClassName = 'white-text'
			style = {
				{
					minWidth: 150,
					maxWidth: 225,
					margin: "5px",
					background: 'var(--vfkr-orange)'
				}
			} >
			< p > < b > ID < /b>: {id}</p >
			< p > < b > Name < /b>: Image {id}</p >
			< p > < b > Tag < /b>: whatever{id}</p >
			< /Card> < /div>
		);
	}
}
