import React, { Component } from 'react';
import '../App.css';
import { IconButton,AppBar,Toolbar,Typography,Breadcrumbs, } from '@material-ui/core';
import MenuIcon from '@material-ui/icons/Menu';
import { Link, BrowserRouter as Router, Route } from 'react-router-dom';
class NavBar extends Component {
  

  render() {
    return (
        <AppBar position="static" color="default" >
        <Toolbar variant="dense">
          <IconButton edge="start" color="inherit" aria-label="menu">
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" color="inherit">
        FBI Emotion
          </Typography>

          <Breadcrumbs aria-label="breadcrumb" id="menu">
            <Link to="/Analyze" class="menuLink">
              Home
            </Link>
            <Link to="/" class="menuLink">
              Logout
            </Link>
          </Breadcrumbs>
        </Toolbar>
      </AppBar>
    );
  }
}

export default NavBar;
