import React, {Component} from "react";
import "../App.css";
import ReactPlayer from "react-player";
import Webcam from "react-webcam";


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
			width='100%'
			height='100%'
			/>
			
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
