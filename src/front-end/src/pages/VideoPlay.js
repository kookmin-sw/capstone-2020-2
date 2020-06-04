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
  Text,
} from 'recharts';

import UserContext from '../UserContext';
import { updateArrayBindingPattern } from 'typescript';
import NavBar from '../components/NavBar';
import railed from '../railed.png';
import { Typography } from '@material-ui/core';

class VideoPlay extends Component {
  constructor(props) {
    super(props);
    this.state = {
      realtimeUserFace: null,
      realtimeStart: 0,
      video: {},
      signalData: [
        {
          emotionTag: 'happiness',
          A: 0.0,
          fullMark: 1.0,
        },
        {
          emotionTag: 'sadness',
          A: 0.0,
          fullMark: 1.0,
        },
        {
          emotionTag: 'disgust',
          A: 0.0,
          fullMark: 1.0,
        },
        {
          emotionTag: 'contempt',
          A: 0.0,
          fullMark: 1.0,
        },
        {
          emotionTag: 'surprise',
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

  redirectToLogin() {
    return this.props.history.push(`/Login`);
  }

  static contextType = UserContext;

  componentWillMount() {
    try {
      const selectedEmotionTag = this.props.location.state.emotionTag;
      console.log(selectedEmotionTag);
      this.setState({
        emotionTag: selectedEmotionTag,
      });
      const { user } = this.context;
      this.setState({
        user: this.context.user,
      });
      console.log('user is', user);
      if (user) {
        console.log('user id', user.id);
        console.log('selectedEmotion', selectedEmotionTag);
        this.getVideo(user.id, selectedEmotionTag);
        this.setState({ realtimeStart: this.state.realtimeStart + 1 });
      } else {
        this.redirectToLogin();
      }
    } catch (error) {
      console.log(error);
      this.props.history.push('/Analyze');
    }
  }
  componentWillUnmount() {
    this.getUserImg = null;
    // this.props.isLast = true;
  }
  componentDidMount() {}

  setRef = (webcam) => {
    this.webcam = webcam;
  };

  getVideo = async (id, emotionTag) => {
    console.log(id, emotionTag);
    try {
      const res = await axios.get(`api/v1/user/${id}/analyze/${emotionTag}/`);
      console.log(res.data);
      const videoData = res.data;
      this.setState({ video: videoData });
      console.log('video is', this.state.video);
    } catch (error) {
      console.log(error.response.message);
    }
  };

  getUserImg = () => {
    const captureImg = setInterval(() => {
      try {
        var base64Str = this.webcam.getScreenshot();
        var file = dataURLtoFile(
          base64Str,
          `${this.state.user.id}-${this.state.video.id}-${(
            '000' + this.state.imageIndex
          ).slice(-3)}.jpg`,
        );
        console.log('getUserImg 실행중');
        this.setState({
          realtimeUserFace: file,
          imageIndex: this.state.imageIndex + 1,
          realtimeStart: this.state.realtimeStart + 1,
        });
        this.realtimeUserFace(file);
        this.eegConnection();
      } catch (error) {
        console.log(error);
      }
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

  realtimeUserFace = (file) => {
    try {
      let realtimeData = new FormData();
      realtimeData.append('image', file);
      realtimeData.append('dateDirPath', this.state.video.dateDirPath);
      realtimeData.append('videoTag', this.state.video.tag);
      console.log('realtimeUserFace image file', file);
      console.log(this.state.video.dateDirPath);
      // console.log('testing....', this.state.realtimeUserFace);
      return (
        axios
          // .get(`api/v1/user/${id}/analyze/real-time-result/`, image, {
          .post(`api/v1/user/analyze/real-time-result/`, realtimeData, {
            headers: {
              'content-type': 'multipart/form-data',
            },
          })
          .then((response) => {
            if (response.data.emotionValues) {
              let values = response.emotionValues;
              console.log(response);
              // console.log(response.data);
              let newSignalData = this.state.signalData;
              console.log(newSignalData);
              const emotionList = [
                'happiness',
                'sadness',
                'disgust',
                'contempt',
                'surprise',
                'fear',
                'neutral',
              ];
              for (let emotionIdx = 0; emotionIdx < 7; emotionIdx++) {
                newSignalData[emotionIdx].A =
                  response.data.emotionValues[emotionList[emotionIdx]];
              }
              let _badConnection = [];
              for (let i = 1; i <= 8; i++) {
                if (response.data.eegConnections[i] === 1) {
                  _badConnection.push(i);
                } else {
                  _badConnection.push('None');
                }
              }
              _badConnection = _badConnection.join(',');
              this.setState({
                signalData: newSignalData,
                badConnection: _badConnection,
              });
            }
          })
      );
    } catch (error) {
      console.log(error);
    }
  };
  eegConnection = async () => {
    const response = await axios
      .get(`api/v1/user/analyze/real-time-result/`)
      .then((response) => {
        let badConnection = [];
        for (let i = 1; i <= 8; i++) {
          if (response.data.eegConnections[i] === 1) {
            badConnection.push(i);
          } else {
            badConnection.push('None');
          }
        }
        badConnection = badConnection.join(',');
      })
      .catch((error) => console.log(error));
  };
  getEmotions = async (id, emotionTag) => {
    const response = await axios
      .get(`api/v1/user/${id}/analyze/${emotionTag}/result/`)
      .then((response) => console.log(response))
      .catch((error) => console.log(error));
    this.append(response);
  };

  render() {
    if (this.state.realtimeStart == 1) {
      this.getUserImg();
    }

    return (
      <div class="full-container">
        <NavBar />
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
        <img src={railed} id="railed"></img>
        <Typography variant="subtitle2" id="connection">
          BadConnection Railed :{' '}
        </Typography>
        <Typography variant="subtitle2" id="connections">
          {this.state.badConnection}{' '}
        </Typography>
        <RadarChart
          outerRadius={68}
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
