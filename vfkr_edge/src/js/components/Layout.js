import React, { Component } from 'react';

import Content from "./Content";
import Footer from "./Footer";
import Header from "./Header";

export default class Layout extends React.Component {
  render() {
    return (
      <div style={{
            height: "100%"
          }}>
        <div style={{
            display: "flex",
            height: "100vh",
            flexDirection: "column"
          }}>
          <div style={{
            flex: 0,
            alignItems: "stretch"
          }}>
            <Header />
          </div> 
          <div style={{
            flex: 1,
            alignItems: "stretch"
          }}>
            <Content />
          </div> 
        </div>
        <div style={{
          position: "absolute",
          bottom: 0,
          width: "100%"
        }}>
          <Footer />
        </div> 
      </div>
    );
  }
}
