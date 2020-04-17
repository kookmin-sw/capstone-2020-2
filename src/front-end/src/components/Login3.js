import React, { Component } from 'react';
import axios from 'axios';
import Webcam from 'react-webcam';
import '../App.css';
import { Spinner, Button,Label} from 'reactstrap';
import { Link ,BrowserRouter as Router, Route, Switch} from 'react-router-dom';


class Login3 extends Component {
  constructor(props) {
    super(props);
    this.state = {
      userName: '',
    };

  }

 userNameChange(event) {
  this.setState({userName: event.target.value});
  console.log(this.state.userName)
}

signupSubmit() {
  console.log("User Name: " + this.state.userName)
  console.log(this.props.location.state)
  // Todo: post username and userFace
  this.signUpRequest()
}

signUpRequest = async () => {
    console.log(this.props.location.state.userFace)
    console.log(this.state.userName)
    let user_form_data = new FormData();
    user_form_data.append('userFace', this.props.location.state.userFace)
    user_form_data.append('username', this.state.userName)
    console.log(user_form_data)
  try {
    const response = await axios.post('api/v1/signup/', user_form_data, {
    headers: {
      'content-type': 'multipart/form-data'
    }
  })
  console.log(response);
  console.log("Sign up 성공");
} catch (error) {
  console.error(error.content);
  console.log("Sign up 실패");
}
};

 render() {
     return (

      <div class = "container-fluid">
      <div class = "row">


         <div class ="col-4" id="login" >
         <>


      <Webcam class = "webcam"
        audio={false}
        facingmode ="user"
        ref={this.loginRef}
        screenshotFormat = "image/jpeg"
      />


     <div class="input-group" id = "userInput">
     <form name="login-username">
     <div class="input-group-sm-prepend">
    <span class="input-group-text">UserName </span>
  </div>

  <input type="text" value ={this.state.userName}
    onChange= {this.userNameChange.bind(this)}
   class="form-control" aria-describedby="basic-addon1"/>
   <button type="button" label="Sign in" onClick = {this.signupSubmit.bind(this)}>Sign up</button>
  </form>
</div>


      </>

        </div>




    <div class = "col-8" id ="explain">
    <div id="carouselNext" class="carousel slide h-100" data-ride="carousel">
<ol class="carousel-indicators">
  <li data-target="#carouselNext" data-slide-to="0" class="active"></li>
  <li data-target="#carouselNext" data-slide-to="1"></li>
  <li data-target="#carouselNext" data-slide-to="2"></li>
</ol>
<div class="carousel-inner h-100" role="listbox"  >
<div class="carousel-item  h-100 active">
<div class="carousel-caption d-none d-md-block  ">
  <h5>Slide1_LoginExplain</h5>
  <p>사용자 얼굴인식으로 로그인/등록이 진행된다.감정인식분석 하자.</p>
</div>
</div>
<div class="carousel-item h-100">
<div class="carousel-caption d-none d-md-block ">
  <h5>slide2_experince function</h5>
  <p>감정인식 체험기능 설명~!@#$$%</p>
</div>
</div>
<div class="carousel-item  h-100">
<div class="carousel-caption d-none d-md-block ">
  <h5>slide3_추천 function</h5>
  <p>감정인식 추천기능 설명~!@#$$%</p>
</div>
</div>
</div>
<a class="carousel-control-prev" href="#carouselNext" role="button" data-slide="prev">
  <span class="carousel-control-prev-icon" aria-hidden="true"></span>
  <span class="sr-only">Previous</span>
</a>
<a class="carousel-control-next" href="#carouselNext" role="button" data-slide="next">
  <span class="carousel-control-next-icon" aria-hidden="true"></span>
  <span class="sr-only">Next</span>
</a>
</div>
       </div>
   </div>
   </div>

     );
 }
}


export default Login3;
