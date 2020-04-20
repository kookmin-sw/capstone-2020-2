import React, {Component} from "react";
import "../App.css";
import ReactPlayer from "react-player";
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
		
			<button type ="button" onclick="location.href ='./Option.js'" ><HomeRoundedIcon class = "home"/></button>
			<button type ="button" onclick="location.href ='./Main.js'" ><ExitToAppIcon class = "logout"/></button>
		
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

