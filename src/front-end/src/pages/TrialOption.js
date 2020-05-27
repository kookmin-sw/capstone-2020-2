import React, { Component } from 'react';
import '../App.css';
import {
  Button,
  Grid,
  withStyles,
  Typography,
  IconButton,
} from '@material-ui/core/';
import { Link, BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import MenuIcon from '@material-ui/icons/Menu';
import Breadcrumbs from '@material-ui/core/Breadcrumbs';
import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';
import InputLabel from '@material-ui/core/InputLabel';
import FormControl from '@material-ui/core/FormControl';
import LoginAlert from '../components/loginSuccessAlert';
import UserContext from '../UserContext';



class Trial extends Component {
  state = {
    emotionTag: '',
    close:true
  };


  redirectToLogin() {
    return this.props.history.push(`/Login`);
  }

  static contextType = UserContext;
  render() {
    const { classes } = this.props;
    const { user } = this.context;
    console.log(user);
    return (
      <>
       {user.loggedIn ? (
        <div class="full-container">
       
       
          <div>
          <AppBar position="static" color="default">
            <Toolbar variant="dense">
              <IconButton edge="start" color="inherit" aria-label="menu">
                <MenuIcon />
              </IconButton>
              <Typography variant="h6" color="inherit">
                Select Emotion
              </Typography>

              <Breadcrumbs aria-label="breadcrumb" id="menu">
                <Link to="/Trial" class="menuLink">
                  Home
                </Link>
                <Link to="/" class="menuLink">
                  Logout
                </Link>
              </Breadcrumbs>
            </Toolbar>
          </AppBar>
          <Grid
          container
          id="loginBox"
         
        >
          <Typography variant="h3" id="trialText">Choose an Emotion what you want!</Typography>

          <FormControl variant="filled" id="emotionSelect" >
        <InputLabel id="demo-simple-select-filled-label">Emotion</InputLabel>
        <Select
          labelId="demo-simple-select-filled-label"
          id="demo-simple-select-filled"
        >
          <MenuItem value="">
            <em>Emotion</em>
          </MenuItem>
          <MenuItem > <Link
                to={{ pathname: '/VideoPlay', state: { emotionTag: 'happy' } }}
              >Happy</Link></MenuItem>
          <MenuItem > <Link
                to={{ pathname: '/VideoPlay', state: { emotionTag: 'sad' } }}
              >Sad</Link></MenuItem>
          <MenuItem > <Link
                to={{ pathname: '/VideoPlay', state: { emotionTag: 'angry' } }}
              >Angry</Link></MenuItem>
          <MenuItem > <Link
                to={{ pathname: '/VideoPlay', state: { emotionTag: 'disgust' } }}
              >Disgust</Link></MenuItem>
          <MenuItem > <Link
                to={{ pathname: '/VideoPlay', state: { emotionTag: 'fear' } }}
              >Fear</Link></MenuItem>
          <MenuItem > <Link
                to={{ pathname: '/VideoPlay', state: { emotionTag: 'neutral' } }}
              >Neutral</Link></MenuItem>
        </Select>
      
      </FormControl>

       
          </Grid>
          </div>
              
        </div>
            ) : (
              this.redirectToLogin()
            )}
       
      
      </>
    );
  }
}

export default Trial;
