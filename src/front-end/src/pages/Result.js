import React, { Component } from 'react';
import axios from 'axios';
import '../App.css';
import { Link, BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import {
  Grid,
  Button,
  Input,
  TextField,
  InputAdornment,
  Typography
} from '@material-ui/core';
import {
    PieChart, Pie, Sector, Cell,
  } from 'recharts';
import UserContext from '../UserContext';
import NavBar from '../components/NavBar';

class Result extends Component {
    constructor(props) {
        super(props);
        this.state = {
          signalData: [
            {
              emotionTag: 'happiness',
              multi: 0.0,
              face: 0.0,
              eeg: 0.0,
              fullMark: 1.0,
            },
            {
              emotionTag: 'sadness',
              multi: 0.0,
              face: 0.0,
              eeg: 0.0,
              fullMark: 1.0,
            },
            {
              emotionTag: 'disgust',
              multi: 0.0,
              face: 0.0,
              eeg: 0.0,
              fullMark: 1.0,
            },
            {
              emotionTag: 'fear',
              multi: 0.0,
              face: 0.0,
              eeg: 0.0,
              fullMark: 1.0,
            },
            {
              emotionTag: 'neutral',
              multi: 0.0,
              face: 0.0,
              eeg: 0.0,
              fullMark: 1.0,
            },
          ],
          user: {
            id: 0,
            name: '',
            loggedIn: false,
          },
          emotionTag: null,
          imageIndex: 1,
         
        };
      }

  static contextType = UserContext;

  render() {
    const { user } = this.context;
    return (
      <div class="full-container">
        <NavBar/>
        <Grid container id="loginBox" direction="column" justify="center">
        <Typography variant="h3" id="AnalyzeText">
                Choose an emotion you want!
              </Typography>
        <PieChart width={400} height={400} class ="PieEEG">
        <Pie
          data={this.state.signalData}
          cx={200}
          cy={200}
          startAngle={180}
          endAngle={0}
          outerRadius={80}
          fill="#8884d8"
          dataKey="eeg"
          label
        >
        </Pie>
      </PieChart>
        <PieChart width={400} height={400}>
        <Pie
          data={this.state.signalData}
          cx={200}
          cy={200}
          outerRadius={80}
          fill="#8884d8"
          dataKey="multi"
          label
        >
        </Pie>
      </PieChart>
      <PieChart width={400} height={400}>
        <Pie
          data={this.state.signalData}
          cx={200}
          cy={200}
          startAngle={180}
          endAngle={0}
          outerRadius={80}
          fill="#8884d8"
          dataKey="face"
          label
        >
        </Pie>
      </PieChart>
          
         
        </Grid>{' '}
      </div>
    );
  }
}

export default Result;
