import React, { Component } from 'react';

import Content from "./Content";
import Footer from "./Footer";
import Header from "./Header";

export default class Layout extends React.Component {
  render() {
    return (
      <div>
        <div style={{
          position: "absolute",
          top: 0,
          width: "100%"
        }}>
          <Header />
        </div> 
        <div style={{
          position: "absolute",
          bottom: 0,
          width: "100%"
        }}>
          <Footer />
        </div> 
        <div style={{
          position: "absolute",
          top: 65,
          bottom: 0,
          width: "100%"
        }}>
          <Content />
        </div> 
      </div>
    );
  }
}
