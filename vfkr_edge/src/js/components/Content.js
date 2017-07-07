import React from "react";

import SplitPane from "react-split-pane";

import Images from "./Content/Images";

export default class Content extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      image_ids: [8, 3]
    };
  }

  render() {
    return (
      <div style={{
        height: "inherit"
      }}>
        <SplitPane split="vertical" defaultSize="38%">
          <div style={{
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


