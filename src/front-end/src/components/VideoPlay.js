import React, {Component} from "react";
import "../App.css";
import ReactPlayer from "react-player";
import {Link, BrowserRouter as Router, Route, Switch} from "react-router-dom";
import Webcam from "react-webcam";
import HomeRoundedIcon from "@material-ui/icons/HomeRounded";
import ExitToAppIcon from "@material-ui/icons/ExitToApp";



class VideoPlay extends Component {

	setRef = webcam => {
		this.webcam = webcam;
	};


	render() {
		return (
<>
			<ReactPlayer 
			className = 'videoPlayer'
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
						</>
		);
	} 
}

export default VideoPlay;

