import React, {Component} from "react";
import axios from "axios";
import Webcam from "react-webcam";
import "../App.css";
import {Spinner, Button} from "reactstrap";
import {
	withRouter,
	Link,
	BrowserRouter as Router,
	Route,
	Switch
} from "react-router-dom";
import "base64-to-image";
import {Grid} from "@material-ui/core";
import IntroCarousel from "./IntroCarousel";

class Login extends Component {
	state = {
		userFace: null
	};

	componentDidMount(Webcam) {
		this.getLogin();
	}

	setRef = webcam => {
		this.webcam = webcam;
	};

	faceDetected() {
		this.props.history.push("/Option");
		console.log("얼굴 정보 있음, 로그인 4 페이지로 넘어감");
	}

	faceNotDetected() {
		this.props.history.push("/Signup", {userFace: this.state.userFace});
		console.log("얼굴 정보 없음, 로그인 3 페이지로 넘어감");
	}

	getLogin = async () => {
		console.log("캡처되고있음");
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

		const captureImg = setTimeout(() => {
			var base64Str = this.webcam.getScreenshot();
			var file = dataURLtoFile(base64Str, "hello.jpg");
			console.log(file);
			console.log("캡처됨");
			this.setState({
				userFace: file
			});
			this.userFace();
		}, 5000);
	};

	userFace = async () => {
		let form_data = new FormData();
		form_data.append("userFace", this.state.userFace);
		try {
			const response = await axios.post("api/v1/login/", form_data, {
				headers: {
					"content-type": "multipart/form-data"
				}
			});
			console.log(response);
			this.faceDetected();
		} catch (error) {
			console.error(error);
			this.faceNotDetected();
		}
	};

	render() {
		return (
			<div class="full-container">
					<Grid
						container
						id="loginBox"
						direction="column"
						justify="center"
						alignItems="center"
					>
						<Grid item>
							<Webcam
								class="webcam"
								id="blink"
								audio={false}
								facingmode="user"
								ref={this.setRef}
								screenshotFormat="image/jpeg"
							/>
						</Grid>
						<Grid item>
							<Spinner onLoad={this.capture} color="secondary" id="spinner" />
						</Grid>
						<Grid item>
							<div
								class="alert alert-secondary border-0"
								style={{marginTop: "5%"}}
								id="text"
								role="alert"
							>
								<strong>[안내]</strong> 5초 후 화면이 캡처됩니다.
							</div>
						</Grid>
					</Grid>

					{/* <Grid item xs={12} sm={8} id="explain">
						<IntroCarousel />
					</Grid> */}
			</div>
		);
	}
}

export default withRouter(Login);
