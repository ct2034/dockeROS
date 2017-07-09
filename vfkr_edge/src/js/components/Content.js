import React from "react";

import SplitPane from "react-split-pane";

import Images from "./Content/Images";

export default class Content extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      image_ids: [3, 4, 5, 8, 10]
    };
  }

  render() {
    return (
      <div style={{
        height: "100%",
        overflow: "hidden"
      }}>
        <SplitPane split="vertical" defaultSize="38%">
          <div style={{
            height: "100%",
            overflow: "auto",
            margin: "8px"
          }}>
            <Images ids={this.state.image_ids} />
          </div>
          <div>B</div>
        </SplitPane>
      </div>
    );
  }
}


