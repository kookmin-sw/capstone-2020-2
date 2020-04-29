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
	setRef = webcam => {
		this.webcam = webcam;
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

				<Link to="/Option">
					<HomeRoundedIcon class="home" />
				</Link>
				<Link to="/">
					{"  "}
					<ExitToAppIcon class="logout" />
				</Link>

				<Webcam
					class="videoWebcam"
					audio={false}
					facingmode="user"
					mirrored={true}
					screenshotQuality={1}
					ref={this.setRef}
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