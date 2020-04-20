import React, {Component} from "react";
import "../App.css";

class IntroCarousel extends Component {
	state = {

	};

	

	render() {
		return (
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
		);
	}
}

export default IntroCarousel;
