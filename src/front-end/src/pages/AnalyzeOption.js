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

import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';
import InputLabel from '@material-ui/core/InputLabel';
import FormControl from '@material-ui/core/FormControl';
import LoginAlert from '../components/loginSuccessAlert';
import UserContext from '../UserContext';
import NavBar from '../components/NavBar';


class Analyze extends Component {
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
       <NavBar />
          <LoginAlert userName={user.name}></LoginAlert>
          <Grid
          container
          id="loginBox"
         
        >
          <Typography variant="h3" id="AnalyzeText">Choose an Emotion what you want!</Typography>

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
              
            
           ) : (
             this.redirectToLogin()
            )}
       
      </>
     
  
     ) }
}

export default Analyze;
