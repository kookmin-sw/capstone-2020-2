import React , { Component } from 'react';
import { Jumbotron, Button} from 'reactstrap';
import { Link ,BrowserRouter as Router, Route, Switch} from 'react-router-dom';
import '../App.css';

class Login1 extends Component {

  render() {
  return (

   <div class = "container-fluid">
     <div class = "row">
    
       
        <div class ="col-4" id="login" >
         <Jumbotron id="start">
           <h2>Get started!</h2>
           <p className="lead">이곳에 당신의 얼굴을 보여주세요. EEG와 표정을 이용한 감정인식이 가능합니다.</p>
           <hr className="my-2" />
           <p>수집된 데이터는 삭제되지 않습니다. </p>
           <p className="lead">
           <Link to = "/Login2"><Button  color ="primary">start</Button>  </Link>
           </p>
        </Jumbotron>
       </div>
    

  
        
   <div class = "col-8" id ="explain">
     <div id="carouselNext" class="carousel slide h-100" data-ride="carousel">
<div class="carousel-inner h-100" >
<div class="carousel-item active h-100">

<div class="carousel-caption d-none d-md-block  ">
  <h5>Slide1_LoginExplain</h5>
  <p>사용자 얼굴인식으로 로그인/등록이 진행된다.감정인식분석 하자.</p>
</div>
</div>
<div class="carousel-item ">
<img src="la.jpg" alt="Los Angeles"/>
<div class="carousel-caption d-none d-md-block ">
  <h5>slide2_experince function</h5>
  <p>감정인식 체험기능 설명~!@#$$%</p>
</div>
</div>
<div class="carousel-item ">
<img src="la.jpg" alt="Los Angeles"/>
<div class="carousel-caption d-none d-md-block ">
  <h5>slide3_추천 function</h5>
  <p>감정인식 추천기능 설명~!@#$$%</p>
</div>
</div>
</div>
<a class="carousel-control-prev" href="#carouselNext" data-slide="prev">
  <span class="carousel-control-prev-icon" aria-hidden="true"></span>
  <span class="sr-only">Previous</span>
</a>
<a class="carousel-control-next" href="#carouselNext" data-slide="next">
  <span class="carousel-control-next-icon" aria-hidden="true"></span>
  <span class="sr-only">Next</span>
</a>
</div>
</div>
      </div>
  </div>
  
 
 

 
  );
};
 
}

export default Login1;
