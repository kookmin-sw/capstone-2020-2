import React, { Component } from 'react';
import axios from 'axios';
import Webcam from 'react-webcam';
import '../App.css';
import { Link, BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import {
  Grid,
  Button,
  Input,
  TextField,
  InputAdornment,
} from '@material-ui/core';
import AccountCircle from '@material-ui/icons/AccountCircle';
class Signup extends Component {
  constructor(props) {
    super(props);
    this.state = {
      userName: '',
    };
  }
  
  userNameChange(event) {
    this.setState({
      userName: event.target.value,
    });
    console.log(this.state.userName);
  }

  signupSubmit() {
    console.log('User Name: ' + this.state.userName);
    console.log(this.props.location.state);
    // Todo: post username and userFace
    this.signUpRequest();
  }

  signUpRequest = async () => {
    console.log(this.props.location.state.userFace);
    console.log(this.state.userName);
    let user_form_data = new FormData();
    user_form_data.append('userFace', this.props.location.state.userFace);
    user_form_data.append('username', this.state.userName);
    console.log(user_form_data);
    try {
      const response = await axios.post('api/v1/signup/', user_form_data, {
        headers: {
          'content-type': 'multipart/form-data',
        },
      });
      console.log(response);
      console.log('Sign up 성공');
      this.props.history.push('/Option', {
        userName: this.state.userName,
      });
    } catch (error) {
      console.error(error.content);
      console.log('Sign up 실패 -  사진 다시찍어야함');
      this.props.history.push('/Login');
    }
  };

  render() {
    return (
      <div class="full-container">
        <Grid container id="loginBox" direction="column" justify="center">
          <Grid item>
            <Webcam
              class="webcam"
              audio={false}
              facingmode="user"
              mirrored={true}
              screenshotQuality={1}
              ref={this.loginRef}
              screenshotFormat="image/jpeg"
            />
          </Grid>{' '}
          <Grid item>
            <div class="input-group" id="userInput">
              <TextField
                id="input-with-icon-textfield"
                label="UserName"
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <AccountCircle />
                    </InputAdornment>
                  ),
                }}
              />{' '}
              <Button
                variant="contained"
                label="Sign in"
                style={{
                  margin: '5%',
                }}
                onClick={this.signupSubmit.bind(this)}
              >
                Sign Up{' '}
              </Button>{' '}
            </div>{' '}
          </Grid>{' '}
        </Grid>{' '}
      </div>
    );
  }
}

export default Signup;
