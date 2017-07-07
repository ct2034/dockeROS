import React from "react";

import {Card, Col} from "react-materialize";

export default class Image extends React.Component {
  render() {
    return (
	  <Col style={{
	  	maxWidth: "300px"
	  }}>
			<Card className='blue-grey darken-1' textClassName='white-text' title='Card title' actions={[<a href='#'>This is a link</a>]}>
			I am a very simple card. My ID: {this.props.id}
			</Card>
		</Col>
    );
  }
}
