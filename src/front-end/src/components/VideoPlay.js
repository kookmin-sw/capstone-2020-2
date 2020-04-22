import React, {Component} from "react";
import "../App.css";
import ReactPlayer from "react-player";
import {
	Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  } from 'recharts';
import Webcam from "react-webcam";
import HomeRoundedIcon from "@material-ui/icons/HomeRounded";
import ExitToAppIcon from "@material-ui/icons/ExitToApp";
import {Link, BrowserRouter as Router, Route, Switch} from "react-router-dom";
  
  const data = [
	{
	  emotion: 'Happiness', pv: 2400, fullMark: 10000,
	},
	{
	  emotion: 'anger', pv: 1398, fullMark: 10000,
	},
	{
	  emotion: 'fear',  pv: 9800, fullMark: 10000,
	},
	{
	  emotion: 'disgust', pv: 3908,fullMark: 10000,
	},
	{
	  emotion: 'sadness', pv: 4800, fullMark: 10000,
	},
	{
	  emotion: 'surprise',  pv: 3800, fullMark: 10000,
	},
	{
	  emotion: 'neutral', pv: 4300,fullMark: 10000,
	},
  ];


class VideoPlay extends Component {

	setRef = webcam => {
		this.webcam = webcam;
	};


	render() {
		return (
<>
			<ReactPlayer 
			classemotion = 'videoPlayer'
			url = 'https://www.youtube.com/watch?v=vqNdWSJyD9Y' 
			playing 
			width = '80%'
			height ='730px'
			/>
		
			<Link to ="/Option"><HomeRoundedIcon class = "home"/></Link>
		<Link to ="/">	<ExitToAppIcon class = "logout"/></Link>
		
			<Webcam
				class = 'videoWebcam'
				audio={false}
				facingmode="user"
				ref={this.setRef}
						/>

<RadarChart cx={300} cy={250} outerRadius={150} width={100} height={100} data={data}>
        <PolarGrid />
        <PolarAngleAxis dataKey="emotion" />
        <PolarRadiusAxis />
        <Radar name="Mike" dataKey="pv" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
      </RadarChart>

					</>
		);
	} 
}

export default VideoPlay;

