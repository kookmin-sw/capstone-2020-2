import React, {Component} from "react";
import "../App.css";
import Carousel from "react-bootstrap/Carousel";
import womanImg from "../woman.jpg";
import smileImg from "../smilewoman.jpg";
import boyImg from "../boy.jpg";
class IntroCarousel extends Component {
	render() {
		return (
			<Carousel>
				<Carousel.Item>
					<img
						className="d-block w-100 h-100"
						src={womanImg}
						alt="First slide"
					/>
					<Carousel.Caption>
						<h3>당신의 감정을 알려드릴게요</h3>
						<p>뇌파와 표정을 이용하겠습니다.</p>
					</Carousel.Caption>
				</Carousel.Item>
				<Carousel.Item>
					<img className="d-block w-100" src={boyImg} alt="Second slide" />

					<Carousel.Caption>
						<h3>slide2_experince function</h3>
						<p>감정인식 체험기능 설명~!@#$$%</p>
					</Carousel.Caption>
				</Carousel.Item>
				<Carousel.Item>
					<img className="d-block w-100" src={smileImg} alt="Third slide" />

					<Carousel.Caption>
						<h3>slide3_추천 function</h3>
						<p>감정인식 추천기능 설명~!@#$$%</p>
					</Carousel.Caption>
				</Carousel.Item>
			</Carousel>
		);
	}
}

export default IntroCarousel;
