import React, {Component} from "react";
// import {Jumbotron, Button} from "reactstrap";
import {Link, BrowserRouter as Router, Route, Switch} from "react-router-dom";
import {Button, Card, CardContent, createMuiTheme, Grid, Hidden, responsiveFontSizes, Typography, ThemeProvider} from "@material-ui/core";
import "../App.css";

let theme = createMuiTheme();
theme = responsiveFontSizes(theme);

class Main extends Component {
	render() {
		return (
			<ThemeProvider theme={theme}>
			<div class="container-fluid" > 
				<Grid container style={{height: '900px'}}>
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
					</Grid>
				</Grid>
			</div>
			</ThemeProvider>
		);
	}
}

export default Main;
