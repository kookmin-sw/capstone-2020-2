import React, {Component} from "react";
import IntroCarousel from "./IntroCarousel";
import {Link, BrowserRouter as Router, Route, Switch} from "react-router-dom";
import {
	Button,
	Card,
	CardContent,
	createMuiTheme,
	Grid,
	Hidden,
	responsiveFontSizes,
	Typography,
	ThemeProvider
} from "@material-ui/core";
import "../App.css";

let theme = createMuiTheme();
theme = responsiveFontSizes(theme);

class Main extends Component {
	render() {
		return (
			<ThemeProvider theme={theme}>
				<div class="full-container">
					<Grid container style={{height: "100%"}}>
						<Grid
							item
							container
							xs={12}
							sm={4}
							id="loginBox"
							direction="column"
							justify="center"
							alignItems="center"
						>
							<Card id="startCard">
								<CardContent
									style={{
										height: "100%",
										paddingTop: "8%",
										textAlign: "center"
									}}
								>
									<Grid item style={{marginBottom: "10%"}}>
										<Typography variant="h4" style={{marginBottom: "5%"}}>
											Get started!
										</Typography>
										<Hidden smDown>
											<Typography variant="h6">
												이 곳에 당신의 얼굴을 보여주세요.
												<br />
												EEG와 표정을 이용한 감정인식이 가능합니다.
											</Typography>
										</Hidden>
									</Grid>
									<Grid item>
										<Hidden smDown>
											<hr />
											<Typography
												variant="subtitle1"
												style={{marginTop: "10%"}}
											>
												* 수집된 데이터는 삭제되지 않습니다.
											</Typography>
										</Hidden>
										<Button
											color="primary"
											variant="outlined"
											href="/Login"
											id="startCardBtn"
											style={{margin: "5%"}}
										>
											start
										</Button>
									</Grid>
								</CardContent>
							</Card>
						</Grid>
						<Grid item xs={12} sm={8} id="explain">
							<IntroCarousel />
						</Grid>
					</Grid>
				</div>
			</ThemeProvider>
		);
	}
}

export default Main;
