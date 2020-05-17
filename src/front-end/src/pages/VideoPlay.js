import React, { Component } from 'react';
import axios from 'axios';
import '../App.css';
import ReactPlayer from 'react-player';
import { Link, BrowserRouter as Router, Route } from 'react-router-dom';
import Webcam from 'react-webcam';
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Legend,
} from 'recharts';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import Breadcrumbs from '@material-ui/core/Breadcrumbs';
import UserContext from '../UserContext';

class VideoPlay extends Component {
  constructor(props) {
    super(props);
    this.state = {
      realtimeUserFace: null,
      video: {},
      signalData: [
        {
          emotionTag: 'happy',
          A: 1.0,
          fullMark: 1.0,
        },
        {
          emotionTag: 'sad',
          A: 0.0,
          fullMark: 1.0,
        },
        {
          emotionTag: 'angry',
          A: 0.0,
          fullMark: 1.0,
        },
        {
          emotionTag: 'disgust',
          A: 0.0,
          fullMark: 1.0,
        },
        {
          emotionTag: 'fear',
          A: 0.0,
          fullMark: 1.0,
        },
        {
          emotionTag: 'neutral',
          A: 0.0,
          fullMark: 1.0,
        },
        {
          emotionTag: 'surprise',
          A: 0.0,
          fullMark: 1.0,
        },
      ],
      user: {
        id: 0,
        name: '',
        loggedIn: false,
      },
      emotionTag:null,
      imageIndex: 1,
    };
  }

  redirectToLogin() {
    return this.props.history.push(`/Login`);
  }

  static contextType = UserContext;

  componentWillMount() {
    try {
      const selectedEmotionTag = this.props.location.state.emotionTag;
      console.log(selectedEmotionTag);
      this.setState({
        // user: {id: user.id, loggedIn: user.loggedIn, }
        emotionTag: selectedEmotionTag,
      });
    
      // console.log(this.state.user);
      console.log('this is signalData', this.state.signalData);
    } catch (error) {
      console.log(error);
      this.props.history.push('/Option');
    }


  }
  componentWillUnmount() {
    this.getUserImg = null;
    // this.props.isLast = true;
  }
  componentDidMount() {
    
    const { user } = this.context;
    console.log('user is', user);
    if (user) {
      this.getVideo(user.id,this.state.emotionTag);
      this.getUserImg(user.id, this.state.emotionTag,this.state.video);
    
    } else {
      this.redirectToLogin();
    }
 
  }

  setRef = (webcam) => {
    this.webcam = webcam;
  };

  getVideo = (id,emotionTag) => {
    console.log(id, emotionTag);
    return axios
      .get(`api/v1/user/${id}/analyze/${emotionTag}/`)
      .then((res) => {
        console.log(res.data)
        const videoData = res.data;
        this.setState({ video: videoData });
        console.log('video is', this.state.video);
      })
      .catch((error) => console.log(error));
  };

  getUserImg = (id, emotionTag,video) => {
    const captureImg = setInterval(() => {
      var base64Str = this.webcam.getScreenshot();
      var file = dataURLtoFile(
        base64Str,
        `${id}-${video.id}-${('000' + this.state.imageIndex).slice(
          -3,
        )}.jpg`,
      );
      console.log(id, emotionTag);
      console.log('캡처됨');
      this.setState({
        realtimeUserFace: file,
        imageIndex: this.state.imageIndex + 1,
      });
      this.realtimeUserFace(id);
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

  realtimeUserFace = (id) => {
    try {
      //let image = new FormData();
      //image.append('image', this.state.realtimeUserFace);
      console.log('testing....', this.state.realtimeUserFace);
      return axios
        //.get(`api/v1/user/${id}/analyze/real-time-result/`, image, {
        .post(`api/v1/user/${id}/analyze/real-time-result/`, {
          headers: {
            'content-type': 'multipart/form-data',
          },
        })
        .then((response) => {
          let values = response.emotionValues;
          console.log(response);
        });
    } catch (error) {
      console.log(error);
    }
  };

  randomValues = () => {
    var emotionFunction = function () {
      const randVal = Math.random();
      const { signalData } = this.state;
      this.setState({
        signalData: signalData.map((A) => randVal),
      });
      // for (let emotions in this.state.signalData) {
      // this.state.signalData.map((emotions) => )
      // console.log(emotions);
      // console.log(emotions['A']);
      // emotions.A = Math.random();
      // }
    };
    const values = setInterval(emotionFunction.bind(this), 1000);
  };

  getEmotions = async (id, emotionTag) => {
    const response = await axios
      .get(`api/v1/user/${id}/analyze/${emotionTag}/result/`)
      .then((response) => console.log(response))
      .catch((error) => console.log(error));
    this.append(response);
  };

  render() {
    return (
      <div class="full-container">
        <div>
          <AppBar position="static" color="default">
            <Toolbar variant="dense">
              <IconButton edge="start" color="inherit" aria-label="menu">
                <MenuIcon />
              </IconButton>
              <Typography variant="h6" color="inherit">
                RealTime Emotion
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
        </div>
        <ReactPlayer
          className="videoPlayer"
          url={this.state.video.link}
          playing
          width="80%"
          height="94%"
        />

        <Webcam
          class="videoWebcam"
          audio={false}
          facingmode="user"
          mirrored={true}
          screenshotQuality={1}
          ref={this.setRef}
          screenshotFormat="image/jpeg"
        />

        <RadarChart
          outerRadius={90}
          width={250}
          height={250}
          data={this.state.signalData}
        >
          <PolarGrid />
          <PolarAngleAxis dataKey="emotionTag" />
          <PolarRadiusAxis angle={30} domain={[0, 1.0]} />
          <Radar
            name="emotion"
            dataKey="A"
            stroke="#8884d8"
            fill="#8884d8"
            fillOpacity={0.6}
          />
        </RadarChart>
      </div>
    );
  }
}

export default VideoPlay;
