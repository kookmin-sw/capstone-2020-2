import React, { Component } from 'react';
import axios from 'axios';
import Webcam from 'react-webcam';
import '../App.css';
import { Spinner, Button } from 'reactstrap';
import {
  withRouter,
  Link,
  BrowserRouter as Router,
  Route,
  Switch,
} from 'react-router-dom';
import 'base64-to-image';
import { Grid } from '@material-ui/core';
import UserContext from '../UserContext';
import NavBar from '../components/NavBar';

class Login extends Component {
  constructor(props) {
    super(props);
    this.state = {
      userFace: null,
    };
  }

  static contextType = UserContext;

  componentWillMount(Webcam) {
    this.getLogin();
  }

  setRef = (webcam) => {
    this.webcam = webcam;
  };

  faceDetected(data) {
    console.log(data);
    const { user, setUser } = this.context;
    const newUser = {
      id: data.id,
      name: data.username,
      loggedIn: true,
    };
    setUser(newUser);
    this.props.history.push('/Analyze');
  }

  faceNotDetected() {
    this.props.history.push('/Signup', { userFace: this.state.userFace });
    console.log('얼굴 정보 없음, 로그인 3 페이지로 넘어감');
  }

  faceNotFound() {
    window.location.reload(false);
  }

  getLogin = async () => {
    console.log('캡처되고있음');

    const captureImg = setTimeout(() => {
      var base64Str = this.webcam.getScreenshot();
      var file = dataURLtoFile(base64Str, 'hello.jpg');
      console.log(file);
      console.log('캡처됨');
      this.setState({
        userFace: file,
      });
      this.userFace();
    }, 2000);
    const dataURLtoFile = (dataurl, filename) => {
      var arr = dataurl.split(','),
        mime = arr[0].match(/:(.*?);/)[1],
        bstr = atob(arr[1]),
        n = bstr.length,
        u8arr = new Uint8Array(n);

      while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
      }

      return new File([u8arr], filename, { type: mime });
    };
  };

  userFace = async () => {
    let form_data = new FormData();
    form_data.append('userFace', this.state.userFace);
    try {
      const response = await axios.post('api/v1/login/', form_data, {
        headers: {
          'content-type': 'multipart/form-data',
        },
      });
      console.log(response);
      this.setState({
        userName: response.data.username,
      });
      this.faceDetected(response.data);
    } catch (error) {
      console.log(error);
      console.error(error.response);
      if (error.response.status == 404) {
        // No user info.
        this.faceNotDetected();
      } else if (error.response.status == 406) {
        // First user error occured.
        this.faceNotDetected();
      } else if (error.response.status == 409) {
        // Cannot recognize face on image.
        this.faceNotFound();
      }
    }
  };

  render() {
    return (
      <div class="full-container">
<NavBar/>
        <Grid
          container
          id="loginBox"
          direction="column"
          justify="center"
          alignItems="center"
        > 
          
            <Webcam
              class="webcam"
              audio={false}
              facingmode="user"
              mirrored={true}
              screenshotQuality={1}
              ref={this.setRef.bind(this)}
              screenshotFormat="image/jpeg"
            />
     <p id="faceLogin">Face Login</p>
     <p id="faceLogin2">가만히 화면을 응시해주세요.</p>
     {/* <img src="https://i.ytimg.com/vi/1KGZtWbZtq8/maxresdefault.jpg" height="250px" width="200px"></img> */}
          {/* <Grid item>
            {/* //<Spinner onLoad={this.capture} color="secondary" id="spinner" /
          </Grid> */}
          {/* <Grid item>
            <div
              class="alert alert-secondary border-0"
              // style={{marginTop: "5%"}}
              id="text"
              role="alert"
            >
              {/* <strong>[안내]</strong> 잠시동안 가만히 화면을 응시해주세요. */}
            {/* </div>
          </Grid> */} 
        </Grid>

        {/* <Grid item xs={12} sm={8} id="explain">
						<IntroCarousel />
					</Grid> */}
      </div>
    );
  }
}

export default withRouter(Login);
