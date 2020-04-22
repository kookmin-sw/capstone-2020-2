import React, {Component} from "react";
import "../App.css";
import Carousel from 'react-bootstrap/Carousel'

class IntroCarousel extends Component {

	render() {
		return (
			<Carousel>
  <Carousel.Item >
    <img
      className="d-block w-100 h-100"
      src=""
      alt="First slide"
    />
    <Carousel.Caption>
      <h3>Slide1_LoginExplain</h3>
      <p>사용자 얼굴인식으로 로그인/등록이 진행된다.감정인식분석
											하자.</p>
    </Carousel.Caption>
  </Carousel.Item>
  <Carousel.Item>
    <img
      className="d-block w-100"
      src=""
      alt="Second slide"
    />

    <Carousel.Caption>
      <h3>slide2_experince function</h3>
      <p>감정인식 체험기능 설명~!@#$$%</p>
    </Carousel.Caption>
  </Carousel.Item>
  <Carousel.Item>
    <img
      className="d-block w-100"
      src=""
      alt="Third slide"
    />

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
