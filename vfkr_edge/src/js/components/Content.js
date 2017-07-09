import React from "react";

import SplitPane from "react-split-pane";

import Images from "./Content/Images";
import Devices from "./Content/Devices";

export default class Content extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      image_ids: [3, 4, 5, 8, 10],
      device_ids: [100, 101, 99, 89]
    };
    this.pane_style = {
      height: "100%",
      overflow: "auto",
      margin: "8px"
    };
  }

  render() {
    return (
      <div style={{
        height: "100%",
        overflow: "hidden"
      }}>
        <SplitPane split="vertical" defaultSize="38%">
          <div style={this.pane_style}>
            <Images ids={this.state.image_ids} />
          </div>
          <div style={this.pane_style}>
            <Devices ids={this.state.device_ids} />
          </div>
        </SplitPane>
      </div>
    );
  }
}


