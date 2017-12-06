import React from "react";

export default class Footer extends React.Component {
  render() {
    return (
      <div style={{
        textAlign: "right",
	    margin: "1vh"}}>
      	<img src="vfk.png" alt="VFK" style={{
      		width: "auto",
      		height: "20vh",
			opacity: 0.5}}/>
      </div>
    );
  }
}
