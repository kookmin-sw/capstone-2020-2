import React, { Component } from 'react';
import Login from './pages/Login';
import Main from './pages/Main';
import Signup from './pages/Signup';
import Option from './pages/Option';
import Trial from './pages/TrialOption';
import VideoPlay from './pages/VideoPlay';
import Analyze from './pages/Analyze';
import './App.css';
import axios from 'axios';
import { Link, BrowserRouter as Router, Route, Switch } from 'react-router-dom';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

class App extends Component {
  //     state = {
  //       posts:[]
  //     };

  //     async componentDidMount(){
  //       try {
  //         const res = await fetch('http//127.0.0.1:8000/posts');
  //         const posts = await res.json();
  //         this.setState({
  //           posts
  //         });
  //       } catch (e) {
  //         console.log(e);
  //       }
  //     }

  render() {
    return (
      <Router>
        <Switch>
          <Route exact path="/" component={Main} />
          <Route path="/Login" component={Login} />
          <Route path="/Signup" component={Signup} />
          <Route path="/Option" component={Option} />
          <Route path="/Trial" component={Trial} />
          <Route path="/VideoPlay" component={VideoPlay} />
          <Router path="/Analyze" component={Analyze} />
        </Switch>
      </Router>
    );
  }
}

export default App;
