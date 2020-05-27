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


class Trial extends Component {
  state = {
    emotionTag: '',
  };

  render() {
    return (
      <>
        <div class="full-container">
          <AppBar position="static" color="default">
            <Toolbar variant="dense">
              <IconButton edge="start" color="inherit" aria-label="menu">
                <MenuIcon />
              </IconButton>
              <Typography variant="h6" color="inherit">
                Select Emotion
              </Typography>

              <Breadcrumbs aria-label="breadcrumb" id="menu">
                <Link to="/Option" class="menuLink">
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
                to={{ pathname: '/VideoPlay', state: { emotionTag: 'happy' } }}
              >Sad</Link></MenuItem>
          <MenuItem > <Link
                to={{ pathname: '/VideoPlay', state: { emotionTag: 'happy' } }}
              >Angry</Link></MenuItem>
          <MenuItem > <Link
                to={{ pathname: '/VideoPlay', state: { emotionTag: 'happy' } }}
              >Disgust</Link></MenuItem>
          <MenuItem > <Link
                to={{ pathname: '/VideoPlay', state: { emotionTag: 'happy' } }}
              >Fear</Link></MenuItem>
          <MenuItem > <Link
                to={{ pathname: '/VideoPlay', state: { emotionTag: 'happy' } }}
              >Neutral</Link></MenuItem>
        </Select>
      
      </FormControl>

          {/* <Grid container spacing={2} id="trialOption">
            
          <Paper class="emotion">
              <Link
                to={{ pathname: '/VideoPlay', state: { emotionTag: 'happy' } }}
              >
             
                  <Typography variant="h5">Happy</Typography>
               
              </Link>
              </Paper>
           
              <Link
                to={{ pathname: '/VideoPlay', state: { emotionTag: 'sad' } }}
              >
                  <Paper class="emotion">
                  <Typography variant="h5">Sad</Typography>
                  </Paper>
              </Link>
          
          
              <Link
                to={{ pathname: '/VideoPlay', state: { emotionTag: 'angry' } }}
              >
              <Paper class="emotion">
                  <Typography variant="h5">Angry</Typography>
                  </Paper>
              </Link>
           
              <Link
                to={{
                  pathname: '/VideoPlay',
                  state: { emotionTag: 'disgust' },
                }}
              >
          <Paper class="emotion">
                  <Typography variant="h5">Disgust</Typography>
                  </Paper>
              </Link>
 
              <Link
                to={{ pathname: '/VideoPlay', state: { emotionTag: 'fear' } }}
              >
               <Paper class="emotion">
                  <Typography variant="h5">Fear</Typography>
                  </Paper>
              </Link>
        
        
              <Link
                to={{
                  pathname: '/VideoPlay',
                  state: { emotionTag: 'neutral' },
                }}
              >   <Paper class="emotion">
                  <Typography variant="h5">Neutral</Typography>
               </Paper>
              </Link>
         </Grid>  */}
          </Grid>
        </div>
      </>
    );
  }
}

export default Trial;
