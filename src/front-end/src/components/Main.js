import React, {Component} from "react";
import IntroCarousel from "./IntroCarousel";
import {Link, BrowserRouter as Router, Route, Switch} from "react-router-dom";
import {Button, Card, CardContent, createMuiTheme, Grid, Hidden, responsiveFontSizes, Typography, ThemeProvider} from "@material-ui/core";
import "../App.css";

let theme = createMuiTheme();
theme = responsiveFontSizes(theme);

class Main extends Component {
	render() {
		return (
<<<<<<< HEAD
			<div class="container-fluid">
				<div class="row">
					<div class="col-4" id="login">
						<Jumbotron id="start">
							<h2>Get started!</h2>
							<p className="lead">
								이곳에 당신의 얼굴을 보여주세요. EEG와 표정을 이용한 감정인식이
								가능합니다.
							</p>
							<hr className="my-2" />
							<p>수집된 데이터는 삭제되지 않습니다.</p>
							<p className="lead">
								<Link to="/Login">
									<Button color="primary" >start</Button>
								</Link>
							</p>
						</Jumbotron>
					</div>

					<div class="col-8" id="explain">
						<div
							id="carouselNext"
							class="carousel slide h-100"
							data-ride="carousel"
						>
							<div class="carousel-inner h-100">
								<div class="carousel-item active h-100">
									<div class="carousel-caption d-none d-md-block  ">
										<h5>Slide1_LoginExplain</h5>
										<p>
											사용자 얼굴인식으로 로그인/등록이 진행된다.감정인식분석
											하자.
										</p>
									</div>
								</div>
								<div class="carousel-item ">
									<img src="la.jpg" alt="Los Angeles" />
									<div class="carousel-caption d-none d-md-block ">
										<h5>slide2_experince function</h5>
										<p>감정인식 체험기능 설명~!@#$$%</p>
									</div>
								</div>
								<div class="carousel-item ">
									<img src="la.jpg" alt="Los Angeles" />
									<div class="carousel-caption d-none d-md-block ">
										<h5>slide3_추천 function</h5>
										<p>감정인식 추천기능 설명~!@#$$%</p>
									</div>
								</div>
							</div>
							<a
								class="carousel-control-prev"
								href="#carouselNext"
								data-slide="prev"
							>
								<span
									class="carousel-control-prev-icon"
									aria-hidden="true"
								></span>
								<span class="sr-only">Previous</span>
							</a>
							<a
								class="carousel-control-next"
								href="#carouselNext"
								data-slide="next"
							>
								<span
									class="carousel-control-next-icon"
									aria-hidden="true"
								></span>
								<span class="sr-only">Next</span>
							</a>
						</div>
					</div>
				</div>
=======
			<ThemeProvider theme={theme}>
			<div class="full-container">  
				<Grid container style={{height: '100%'}}>
					<Grid item container xs={12} sm={4} id="loginBox" direction="column" justify="center" alignItems="center">
						<Card id="startCard">
							<CardContent style={{height:"100%", paddingTop: "8%",textAlign: "center"}}>
								<Grid item style={{marginBottom: "10%"}}><Typography variant="h4" style={{marginBottom: "5%"}}>Get started!</Typography>
									<Hidden smDown><Typography variant="h6">
										이 곳에 당신의 얼굴을 보여주세요. 
										<br/>EEG와 표정을 이용한 감정인식이
										가능합니다.
									</Typography></Hidden>
								</Grid>
								<Grid item> 
								<Hidden smDown><hr/>
									<Typography variant="subtitle1" style={{marginTop: "10%"}}>* 수집된 데이터는 삭제되지 않습니다.</Typography></Hidden>
									<Button color="primary" variant="outlined" href="/Login" id="startCardBtn" style={{margin: "5%"}}>start</Button>
								</Grid>
							</CardContent>
						</Card>   
					</Grid>  
					<Grid item xs={12} sm={8} id="explain">
						<IntroCarousel/>
					</Grid>
				</Grid>
>>>>>>> c819d388dee3af9e868f0f1af4faf167bebaf471
			</div>
			</ThemeProvider>
		);
	}
}

export default Main;
