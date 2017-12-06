import React from "react";

export default class Bar extends React.Component {
	render() {
		return ( < div >
			< div style = {
				{
					height: 20,
					width: "100%",
					marginTop: 2,
					backgroundColor: "var(--vfkr-darkgrey)",
					textAlign: "left"
				}
			} >
			< div style = {
				{
					width: this.props.val + "%",
					height: "100%",
					backgroundColor: "var(--vfkr-lightgrey)",
					paddingLeft: 2,
					paddingBottom: 3,
					animationDuration: '0.5s'
				}
			} > {
				this.props.name
			} < /div> < /div> < /div>
		);
	}
}
