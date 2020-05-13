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
  state = {
    realtimeUserFace: null,
    link:'',
    data :
      [
        {
          emotionTag: 'happy', A: 120, B: 110, fullMark: 150,
        },
        {
          emotionTag: 'sad', A: 98, B: 130, fullMark: 150,
        },
        {
          emotionTag: 'angry', A: 86, B: 130, fullMark: 150,
        },
        {
          emotionTag: 'disgust', A: 99, B: 100, fullMark: 150,
        },
        {
          emotionTag: 'fear', A: 85, B: 90, fullMark: 150,
        },
        {
          emotionTag: 'neutral', A: 65, B: 85, fullMark: 150,
        },
      ]
    };

   
 
  static contextType = UserContext;
  
  componentWillMount(){
    const emotionTag = this.props.location.state.emotionTag;
    console.log(emotionTag);
    const { user } = this.context;
    console.log(user);
    const id = user.id;
    console.log(id);
   this.getVideo(id,emotionTag);
   this.getUserImg(id,emotionTag);
  }
  componentWillUnmount() {
    this.getUserImg = null;
    this.props.isLast = true;
  }
  componentDidMount(){

  }
  setRef = webcam => {
    this.webcam = webcam;
  };
  // getUser =async () => {
  //   try{
  //     let form_data = new FormData();
  //  const response = axios.post('api/v1/login/', form_data, {
  //   headers: {
  //     'content-type': 'multipart/form-data',
  //   },
  // }) ;
  //   console.log(response);
  //     this.setState({
  //      id: response.data.id,
  //     });
    
  //   }catch(error){
  //     console.error(error);
  //   }
  // };


    getVideo = (id,emotionTag) => {
     return axios
      .get(`api/v1/user/${id}/trial/${emotionTag}/`)
      .then(res => {
        const video= res.data;
        this.setState({link:video.link});
        console.log(this.state.link)
      })
      .catch(error => console.log(error));
  };

  

  getUserImg = (id,emotionTag) => {
    //console.log("캡처되고있음");



    const captureImg = setInterval(() => {
      var base64Str = this.webcam.getScreenshot();
      var file = dataURLtoFile(
        base64Str,
        `${this.props.id}-001`,
      );
      console.log(file);
      console.log('캡처됨');
      this.setState({
        realtimeUserFace: file,
      });
      this.realtimeUserFace(id,emotionTag);
    }, 1000);

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

  realtimeUserFace = (id,emotionTag) => {
    try{
      const image = new FormData();
      image.append('realtimeUserFace', this.state.realtimeUserFace);
      return axios
        .get(
          `api/v1/user/${id}/trial/${emotionTag}/real-time-result/`,
          image,
          {
            headers: {
              'content-type': 'multipart/form-data',
            },
          },
        )
    } catch(error){
      console.log(error);
    }

     
  };

  getEmotions = async (id, emotionTag) => {
    const response = await axios
      .get(`api/v1/user/${id}/trial/${emotionTag}/result/`)
      .then(response => console.log(response))
      .catch(error => console.log(error));
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
          url= {this.state.link}
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

                                    
<RadarChart outerRadius={90} width={250} height={250} data={this.state.data}>
  <PolarGrid />
  <PolarAngleAxis dataKey="emotionTag" />
  <PolarRadiusAxis angle={30} domain={[0, 150]} />
  <Radar name="emotion" dataKey="A" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
</RadarChart>
      </div>
    );
  }
};

export default VideoPlay;