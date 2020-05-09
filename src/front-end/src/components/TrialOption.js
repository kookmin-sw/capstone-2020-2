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
                Trial_Select Emotion
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

          <Grid container spacing={2} id="trialOption">
            <Grid item xs={4}>
              <Link
                to={{ pathname: '/VideoPlay', state: { emotionTag: 'happy' } }}
              >
                <Button value="happy" color="primary" variant="contained">
                  <Typography variant="h5">Happy</Typography>
                </Button>
              </Link>
            </Grid>
            <Grid item xs={4}>
              <Link
                to={{ pathname: '/VideoPlay', state: { emotionTag: 'sad' } }}
              >
                <Button value="sad" color="primary" variant="contained">
                  <Typography variant="h5">Sad</Typography>
                </Button>
              </Link>
            </Grid>
            <Grid item xs={4}>
              <Link
                to={{ pathname: '/VideoPlay', state: { emotionTag: 'angry' } }}
              >
                <Button value="angry" color="primary" variant="contained">
                  <Typography variant="h5">Angry</Typography>
                </Button>
              </Link>
            </Grid>
            <Grid item xs={4}>
              <Link
                to={{
                  pathname: '/VideoPlay',
                  state: { emotionTag: 'disgust' },
                }}
              >
                <Button value="disgust" color="primary" variant="contained">
                  <Typography variant="h5">Disgust</Typography>
                </Button>
              </Link>
            </Grid>
            <Grid item xs={4}>
              <Link
                to={{ pathname: '/VideoPlay', state: { emotionTag: 'fear' } }}
              >
                <Button value="fear" color="primary" variant="contained">
                  <Typography variant="h5">Fear</Typography>
                </Button>
              </Link>
            </Grid>
            <Grid item xs={4}>
              <Link
                to={{
                  pathname: '/VideoPlay',
                  state: { emotionTag: 'neutral' },
                }}
              >
                <Button value="neutral" color="primary" variant="contained">
                  <Typography variant="h5">Neutral</Typography>
                </Button>
              </Link>
            </Grid>
          </Grid>
        </div>
      </>
    );
  }
}

export default Trial;
