import React from "react";

export default class Bar extends React.Component {
  render() {
    return (
		<div>
			<div className='progress-bg' style={{
				height: 20,
				width: "100%",
				marginTop: 2,
				backgroundColor: "gray",
				textAlign: "left",
			}} >
				<div className='progress-bar' style={{
					width: this.props.val+"%",
					height: "100%",
					backgroundColor: "darkgray",
					paddingLeft: "2"
				}}>
				{this.props.name}
				</div>
			</div>
		</div>
    );
  }
}
