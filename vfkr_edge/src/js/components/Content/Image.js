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

		getContent() {
			return ([ < p key = "1" > < b > ID < /b>: {this.props.id} < /p > , 
				< p key = "2" > < b > Name < /b>: Image {this.props.id} < /p > , 
				< p key = "3" > < b > Tag < /b>: whatever{this.props.id} < /p > ]);
		}

		render() {
			const {
				id,
				connectDragSource,
				isDragging,
				inDeviceCollapsible
			} = this.props;

			// console.log(this.props)

			if (inDeviceCollapsible) {
				return ( < div > {
						this.getContent()
					} < /div>)
				}
				else {

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
						} > {
							this.getContent()
						} < /Card> < /div >
					);
				}
			}
		}
