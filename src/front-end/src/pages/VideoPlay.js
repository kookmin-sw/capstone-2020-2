import React, { Component } from 'react';
import axios from 'axios';
import '../App.css';
import ReactPlayer from 'react-player';
import { Link, BrowserRouter as Router, Route } from 'react-router-dom';
import Webcam from 'react-webcam';
import {
  ComposedChart,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Area,
  Bar,
  Line,
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Legend,
  Text,
} from 'recharts';

import UserContext from '../UserContext';
import { updateArrayBindingPattern, setTokenSourceMapRange } from 'typescript';
import NavBar from '../components/NavBar';
import railed from '../railed.png';
import { Typography, Grid } from '@material-ui/core';

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
          multi: 10.0,
          face: 0.0,
          eeg: 0.0,
        },
        {
          emotionTag: 'sadness',
          multi: 0.0,
          face: 0.0,
          eeg: 0.0,
        },
        {
          emotionTag: 'disgust',
          multi: 0.0,
          face: 0.0,
          eeg: 0.0,
        },
        {
          emotionTag: 'fear',
          multi: 0.0,
          face: 0.0,
          eeg: 0.0,
        },
        {
          emotionTag: 'neutral',
          multi: 0.0,
          face: 0.0,
          eeg: 0.0,
        },
      ],
      user: {
        id: 0,
        name: '',
        loggedIn: false,
      },
      emotionTag: null,
      imageIndex: 1,
      fullConnected: false,
      badConnection: {
        eeg1: 1,
        eeg2: 1,
        eeg3: 1,
        eeg4: 1,
        eeg5: 1,
        eeg6: 1,
        eeg7: 1,
        eeg8: 1,
      },
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
      // this.eegConnection();
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
      console.log(this.state.badConnection);
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
              // let newSignalData = this.state.signalData;
              let newSignalData = [];
              console.log(newSignalData);
              const emotionList = [
                'happiness',
                'sadness',
                'disgust',
                'fear',
                'neutral',
              ];
              for (let emotionIdx = 0; emotionIdx < 5; emotionIdx++) {
                newSignalData.push({
                  emotionTag: emotionList[emotionIdx],
                  multi: response.data.emotionValues[emotionList[emotionIdx]],
                  face: response.data.faceValues[emotionList[emotionIdx]],
                  eeg: response.data.eegValues[emotionList[emotionIdx]],
                });
                // newSignalData[emotionIdx].emotionTag = emotionList[emotionIdx];
                // newSignalData[emotionIdx].multi =
                //   response.data.emotionValues[emotionList[emotionIdx]];
                // newSignalData[emotionIdx].face =
                //   response.data.faceValues[emotionList[emotionIdx]];
                // newSignalData[emotionIdx].eeg =
                //   response.data.eegValues[emotionList[emotionIdx]];
              }
              let _badConnection = response.data.eegConnections;
              let eegCheck = true;
              for (let eegIdx = 1; eegIdx < 8; eegIdx++) {
                if (response.data.eegConnections['eeg' + eegIdx] == 1) {
                  eegCheck = false;
                }
              }
              console.log(this.state.badConnection);
              this.setState({
                signalData: newSignalData,
                badConnection: _badConnection,
                fullConnected: eegCheck,
              });
            }
          })
      );
    } catch (error) {
      console.log(error);
    }
  };
  // eegConnection = async () => {
  //   let badConnection = [];
  //   for (let i = 1; i <= 8; i++) {
  //     if (response.data.eegConnections[i] === 1) {
  //       badConnection.push(i);
  //     } else {
  //       badConnection.push('None');
  //     }
  //   }
  //   badConnection = badConnection.join(',');
  // };
  // getEmotions = async (id, emotionTag) => {
  //   const response = await axios
  //     .get(`api/v1/user/${id}/analyze/${emotionTag}/result/`)
  //     .then((response) => console.log(response))
  //     .catch((error) => console.log(error));
  //   this.append(response);
  // };

  render() {
    // if (this.state.realtimeStart == 1) {
    //   this.getUserImg();
    // }
    console.log(this.state.signalData);
    let connection = this.state.badConnection;
    const varFromState = this.state.signalChange;
    return (
      <div class="full-container">
        <NavBar />
        {/* <div id="real-time-box"> */}

        <Grid container>
          <Grid item xs={9}>
            <ReactPlayer
              width="1390px"
              height="925px"
              className="videoPlayer"
              url={this.state.video.link}
              playing
            />
          </Grid>
          <Grid item xs={3} container direction="column">
            <Grid item xs>
              <Webcam
                class="videoWebcam"
                audio={false}
                facingmode="user"
                mirrored={true}
                screenshotQuality={1}
                ref={this.setRef}
                screenshotFormat="image/jpeg"
              />
            </Grid>
            <Grid item container xs>
              <Grid item xs={6}>
                <img src={railed} id="railed"></img>
              </Grid>
              {this.state.fullConnected ? (
                <Grid item xs={6}>
                  <Typography variant="subtitle2" id="connection">
                    All sensors are connected!
                  </Typography>
                </Grid>
              ) : (
                <Grid item xs={6}>
                  <Typography variant="subtitle2" id="connection">
                    BadConnection Railed :
                  </Typography>
                  <Typography variant="subtitle2" id="connections">
                    {connection.eeg1 ? '1 ' : ''}
                    {connection.eeg2 ? '2 ' : ''}
                    {connection.eeg3 ? '3 ' : ''}
                    {connection.eeg4 ? '4 ' : ''}
                    {connection.eeg5 ? '5 ' : ''}
                    {connection.eeg6 ? '6 ' : ''}
                    {connection.eeg7 ? '7 ' : ''}
                    {connection.eeg8 ? '8 ' : ''}
                    {/* {this.state.badConnection} */}
                  </Typography>
                </Grid>
              )}
            </Grid>
            {/* <RadarChart
            id="realtimeChart"
            outerRadius={68}
            width={250}
            height={250}
            data={this.state.signalData}
          >
            <PolarGrid />
            <PolarAngleAxis dataKey="emotionTag" />
            <PolarRadiusAxis angle={18} domain={[0, 1.0]} />
            <Radar
              name="emotion"
              dataKey="multi"
              stroke="#ff6f69"
              fill="#ff6f69"
              fillOpacity={0.6}
            />
            <Radar
              name="EEG"
              dataKey="eeg"
              stroke="#ffdd77"
              fill="#ffdd77"
              fillOpacity={0.6}
            />
            <Radar
              name="Face"
              dataKey="face"
              stroke="#96ceb4"
              fill="#96ceb4"
              fillOpacity={0.6}
            />
          </RadarChart>{' '} */}
            <Grid>
              <ComposedChart
                // id="realtimeChart"
                width={430}
                height={330}
                data={this.state.signalData}
                style={{ marginTop: '5%' }}
              >
                <XAxis dataKey="emotionTag" />
                <YAxis />
                <Tooltip />
                <Legend />
                <CartesianGrid stroke="#f5f5f5" />
                <Area
                  type="monotone"
                  name="Face"
                  dataKey="face"
                  fill="#F5F7FA"
                  stroke="#ffc2c2"
                />
                <Area
                  type="monotone"
                  name="EEG"
                  dataKey="eeg"
                  fill="#F5F7FA"
                  stroke="#86c1e0"
                />
                <Bar name="Multi" dataKey="multi" barSize={20} fill="#554475" />
              </ComposedChart>
            </Grid>
          </Grid>
        </Grid>
        {/* <ComposedChart width={300} height={250} data={this.state.signalData}>
            <CartesianGrid stroke="#f5f5f5" />
            <XAxis dataKey="emotionTag" />
            <YAxis key={varFromState} />
            <Tooltip />
            <Legend />
            <Area
              type="monotone"
              dataKey="multi"
              fill="gray"
              stroke="#8884d8"
            />
            <Bar dataKey="face" barSize={20} fill="#413ea0" />
            <Line type="monotone" dataKey="eeg" stroke="#ff7300" />
          </ComposedChart> */}
      </div>
    );
  }
}

export default VideoPlay;
