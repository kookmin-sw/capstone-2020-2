import React, { Component } from 'react';
import '../App.css';
import Carousel from 'react-bootstrap/Carousel';
import carouselImage1 from './Image/carouselImage1';
import carouselImage2 from './Image/carouselImage2';
import carouselImage3 from './Image/carouselImage3';

class IntroCarousel extends Component {
  render() {
    return (
<Carousel>
        <Carousel.Item style={{ height: '100%' }}>
          <img
            className="d-block w-100 h-100"
            src={carouselImage1}
            alt="First slide"
          />
          <Carousel.Caption>
            <h3>slide1_Intro</h3>
            <p>로그인 기능 설명란 구성 예정</p>
          </Carousel.Caption>
        </Carousel.Item>
        <Carousel.Item style={{ height: '100%' }}>
          <img
            className="d-block w-100 h-100"
            src={carouselImage2}
            alt="Second slide"
          />

          <Carousel.Caption>
            <h3>slide2_체험 설명</h3>
            <p>감정인식 체험기능 설명란 구성 예정</p>
          </Carousel.Caption>
        </Carousel.Item>
        <Carousel.Item style={{ height: '100%' }}>
          <img
            className="d-block w-100 h-100"
            src={carouselImage3}
            alt="Third slide"
          />

          <Carousel.Caption>
            <h3>slide3_추천 설명</h3>
            <p>감정인식 추천기능 설명란 구성 예정</p>
          </Carousel.Caption>
        </Carousel.Item>
      </Carousel>
    );
  }
}

export default IntroCarousel;
