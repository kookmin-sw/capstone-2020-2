import React, { Component } from 'react';
import '../App.css';
import Carousel from 'react-bootstrap/Carousel';
import carouselImage1 from './Image/carouselImage1';
import carouselImage2 from './Image/carouselImage2';
import carouselImage3 from './Image/carouselImage3';
import carouselImage4 from './Image/carouselImage4';

class IntroCarousel extends Component {
  render() {
    return (
      <Carousel>
        <Carousel.Item style={{ height: '100%' }}>
          <img className="d-block w-100 h-100" src={carouselImage1} />
        </Carousel.Item>
        <Carousel.Item style={{ height: '100%' }}>
          <img className="d-block w-100 h-100" src={carouselImage2} />
        </Carousel.Item>
        <Carousel.Item style={{ height: '100%' }}>
          <img className="d-block w-100 h-100" src={carouselImage3} />
        </Carousel.Item>
        <Carousel.Item style={{ height: '100%' }}>
          <img className="d-block w-100 h-100" src={carouselImage4} />
        </Carousel.Item>
      </Carousel>
    );
  }
}

export default IntroCarousel;
