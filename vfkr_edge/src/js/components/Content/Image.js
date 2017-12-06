import React from "react";

import {
	Card,
	Col,
	Button
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

		constructor(props) {
			super(props);
			this.state = {
				tags: [],
				architecture: 'tdb',
				deployable: true
			};
			this.props.emitter.addListener('deploy', (name) => {
				console.log(name);
				if(this.props.name != name){
					this.setState({deployable: false})
				}
			});
			this.props.emitter.addListener('deployed_to', (name) => {
				// console.log(name);
				this.setState({deployable: true})
			});
			// this.update()
		}

		update() {
			$.get("http://localhost:5000/v2/"+this.props.name+"/tags/list", function(data, status) {
				if (status == 'success') {
					this.setState({
						tags: data['tags']
					});
				}
			}.bind(this));
			$.get("http://localhost:5000/v2/"+this.props.name+"/manifests/latest", function(data, status) {
				if (status == 'success') {
					const architecture = JSON.parse(data)["architecture"]
					this.setState({
						architecture
					});
				}
			}.bind(this));

			setTimeout(this.update.bind(this), 1000);
		}

		getContent() {
			return ([ 
				< p key = "name" > < b > Name< /b>: {this.props.name} < /p > , 
				< p key = "architecture" > < b > Architecture< /b>: {this.state.architecture} < /p > ,
				< div key = "tags" > < b > Tags< /b>: {
					this.state.tags.map((tag) => <div style={{
						overflow: "hidden",
						wordBreak: "keep-all",
						fontStyle: ((tag == "latest") ? 'italic' : 'normal')
					}} key={tag} > {tag.substring(0, 20)} </div>)
				} < /div > ]);
		}

		render() {
			const {
				name,
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
								overflowWrap: "break-word",
								background: 'var(--vfkr-orange)'
							}
						} > 
							< img src={(name.startsWith("ros")) ? "ros.png" : "app.png"} alt="ROS Logo" height="30" width="30" style={{
								marginBottom: "6px"
							}}/> {
							this.getContent()
						}
						<Button floating className="black" disabled={
							(this.state.deployable) ? (false) : (true)
						} onClick={function() {
							this.props.emitter.emit('deploy', name);
							console.log("emit deploy " + name);
							Materialize.toast('Please select device to deploy to', 4000);
						}.bind(this)} icon='play_arrow'
						style={{
							    position: "absolute",
							    right: 1,
							    bottom: "-6",
							    height: "38px",
							    padding: 0
						}} />
						< /Card> < /div >
					);
				}
			}
		}
