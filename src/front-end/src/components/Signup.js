import React, {Component} from "react";
import axios from "axios";
import Webcam from "react-webcam";
import "../App.css";
import {Link, BrowserRouter as Router, Route, Switch} from "react-router-dom";
import {Grid} from "@material-ui/core";
import IntroCarousel from "./IntroCarousel";
class Signup extends Component {
	constructor(props) {
		super(props);
		this.state = {
			userName: ""
		};
	}

	userNameChange(event) {
		this.setState({userName: event.target.value});
		console.log(this.state.userName);
	}

	signupSubmit() {
		console.log("User Name: " + this.state.userName);
		console.log(this.props.location.state);
		// Todo: post username and userFace
		this.signUpRequest();
	}

	signUpRequest = async () => {
		console.log(this.props.location.state.userFace);
		console.log(this.state.userName);
		let user_form_data = new FormData();
		user_form_data.append("userFace", this.props.location.state.userFace);
		user_form_data.append("username", this.state.userName);
		console.log(user_form_data);
		try {
			const response = await axios.post("api/v1/signup/", user_form_data, {
				headers: {
					"content-type": "multipart/form-data"
				}
			});
			console.log(response);
			console.log("Sign up 성공");
			this.props.history.push("/Option");
		} catch (error) {
			console.error(error.content);
			console.log("Sign up 실패 - 사진 다시찍어야함");
			this.props.history.push("/Login");
		}
	}; 

	render() {
		return (
			<div class="full-container">
				<Grid container direction="row" style={{height: '100%'}}> 
					<Grid item container xs={12} sm={4} id="loginBox" direction="column" justify="center">
						<Grid item >
							<Webcam
								class="webcam"
								audio={false}
								facingmode="user"
								ref={this.loginRef}
								screenshotFormat="image/jpeg"
							/>
                        </Grid>
                        <Grid item>
							<div class="input-group" id="userInput">
								<form name="login-username">
									<div class="input-group-sm-prepend">
										<span class="input-group-text">UserName </span>
									</div>

									<input
										type="text"
										value={this.state.userName}
										onChange={this.userNameChange.bind(this)}
										class="form-control"
										aria-describedby="basic-addon1"
									/>
									<button
										type="button"
										label="Sign in"
										style={{margin: "5%"}}
										onClick={this.signupSubmit.bind(this)}
									>
										Sign up
									</button>
								</form>
							</div>
						</Grid>
					</Grid>

					<Grid item xs={12} sm={8} id="explain">
						<IntroCarousel/>
					</Grid>
				</Grid>
			</div>
		);
	}
}

export default Signup;
