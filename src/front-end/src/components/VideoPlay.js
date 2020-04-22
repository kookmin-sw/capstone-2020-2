import React, {Component} from "react";
import "../App.css";
import ReactPlayer from "react-player";
import {
	withRouter,
	Link,
	BrowserRouter as Router,
	Route,
	Switch
} from "react-router-dom";
import Webcam from "react-webcam";
import HomeRoundedIcon from "@material-ui/icons/HomeRounded";
import ExitToAppIcon from "@material-ui/icons/ExitToApp";
import {
	BarChart,
	Bar,
	XAxis,
	YAxis,
	CartesianGrid,
	Tooltip,
	Legend
} from "recharts";

const data = [
	{
		name: "Happiness",
		pv: 2400,
		amt: 2400
	},
	{
		name: "anger",
		pv: 1398,
		amt: 2210
	},
	{
		name: "fear",
		pv: 9800,
		amt: 2290
	},
	{
		name: "disgust",
		pv: 3908,
		amt: 2000
	},
	{
		name: "sadness",
		pv: 4800,
		amt: 2181
	},
	{
		name: "surprise",
		pv: 3800,
		amt: 2500
	},
	{
		name: "neutral",
		pv: 4300,
		amt: 2100
	}
];

class VideoPlay extends Component {
	setRef = webcam => {
		this.webcam = webcam;
	};

	render() {
		return (
			<div class="full-container">
				<ReactPlayer
					className="videoPlayer"
					url="https://www.youtube.com/watch?v=vqNdWSJyD9Y"
					playing
					width="80%"
					height="100%"
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
					ref={this.setRef}
				/>

				<BarChart width={300} height={300} data={data} barSize={20}>
					{" "}
					<XAxis dataKey="name" scale="point" padding={{left: 10, right: 10}} />
					<Tooltip />
					<Legend />
					<CartesianGrid strokeDasharray="3 3" />
					<Bar dataKey="pv" fill="#8884d8" background={{fill: "#eee"}} />
				</BarChart>
			</div>
		);
	}
}

export default VideoPlay;
