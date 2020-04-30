import React, {Component} from "react";
import "../App.css";
import ReactPlayer from "react-player";
import {
	Link,
	BrowserRouter as Router,
	Route,
} from "react-router-dom";
import Webcam from "react-webcam";
import HomeRoundedIcon from "@material-ui/icons/HomeRounded";
import ExitToAppIcon from "@material-ui/icons/ExitToApp";
import {
	Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  } from 'recharts';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import Breadcrumbs from '@material-ui/core/Breadcrumbs';



const data = [
	{
		name: "Happiness",
		A: 86,
		fullMark: 100
	},
	{
		name: "anger",
		A: 17,
		fullMark: 100
	},
	{
		name: "fear",
		A: 29,
		fullMark: 100
	},
	{
		name: "disgust",
		A: 46,
		fullMark: 100
	},
	{
		name: "sadness",
		A: 23,
		fullMark: 100
	},
	{
		name: "surprise",
		A: 45,
		fullMark: 100
	},
	{
		name: "neutral",
		A: 56,
		fullMark: 100
	}
];

class VideoPlay extends Component {

	state = {
		realtimeUserFace: null
	};

	componentDidMount(Webcam) {
		this.getUserImg();
	}

	setRef = webcam => {
		this.webcam = webcam;
	};

	getUserImg = async () => {
		//console.log("캡처되고있음");
		
		const dataURLtoFile = (dataurl, filename) => {
			var arr = dataurl.split(","),
				mime = arr[0].match(/:(.*?);/)[1],
				bstr = atob(arr[1]),
				n = bstr.length,
				u8arr = new Uint8Array(n);

			while (n--) {
				u8arr[n] = bstr.charCodeAt(n);
			}

			return new File([u8arr], filename, {type: mime});
		};

		const captureImg = setInterval(() => {
			var base64Str = this.webcam.getScreenshot();
			var file = dataURLtoFile(base64Str, "hello.jpg");
			console.log(file);
			console.log("캡처됨");
			this.setState({
				realtimeUserFace: file
			});
			this.realtimeUserFace();
		}, 1000);
		
	};
	
	realtimeUserFace = async () => {
		let form_data = new FormData();
		form_data.append("userFace", this.state.userFace);
		try {
			const response = await axios.post("api/v1/login/", form_data, {
				headers: {
					"content-type": "multipart/form-data"
				}
			});
			console.log(response);
			this.setState({
				userName: response.data.username
			})
			this.faceDetected();
		} catch (error) {
			console.error(error);
			this.faceNotDetected();
		}
	};
	
	render() {
		return (
			<div class="full-container">
				<div >
      <AppBar position="static" color = "default">
        <Toolbar variant="dense">
          <IconButton edge="start"  color="inherit" aria-label="menu">
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" color="inherit">
            RealTime Emotion
          </Typography>
		  
<Breadcrumbs aria-label="breadcrumb" id ="menu">
      <Link to="/Option" class ="menuLink" >
        Home
      </Link>
      <Link to="/" class ="menuLink" >
      Logout
      </Link>
    </Breadcrumbs>
        </Toolbar>
      </AppBar>
    </div>	
				<ReactPlayer
					className="videoPlayer"
					url="https://www.youtube.com/watch?v=vqNdWSJyD9Y"
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

<RadarChart cx={300} cy={250} outerRadius={150} width={500} height={500} data={data}>
        <PolarGrid />
        <PolarAngleAxis dataKey="name" />
        <PolarRadiusAxis />
        <Radar dataKey="A" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
      </RadarChart>
			</div>
		);
	}
}

export default VideoPlay;