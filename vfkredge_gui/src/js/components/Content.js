import React from "react";

import SplitPane from "react-split-pane";
import { DragDropContext } from 'react-dnd';
import { default as TouchBackend } from 'react-dnd-touch-backend';
import {EventEmitter} from 'fbemitter';

import Images from "./Content/Images";
import Devices from "./Content/Devices";

@DragDropContext(TouchBackend)
export default class Content extends React.Component {

  constructor(props) {
    super(props);
    this.pane_style = {
      height: "100%",
      overflow: "auto",
      margin: "8px"
    };
    this.emitter = new EventEmitter(); 
  }

  render() {
    return (
      <div style={{
        height: "100%",
        overflow: "hidden"
      }}>
        <SplitPane split="vertical" defaultSize="38%">
          <div style={this.pane_style}>
            <Images emitter={this.emitter}/>
          </div>
          <div style={this.pane_style}>
            <Devices emitter={this.emitter}/>
          </div>
        </SplitPane>
      </div>
    );
  }
}


