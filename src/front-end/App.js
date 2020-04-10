import React, { Component } from 'react';
import Login1 from './components/Login1';
import Login2 from './components/Login2';
import Login3 from './components/Login3';
import Trial from './components/Trial';
import './App.css';
import { Jumbotron, Button} from 'reactstrap';
import { Link ,BrowserRouter as Router, Route, Switch} from 'react-router-dom';


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
    <Route exact path='/' component={Login1}/>
    <Route path='/Login2' component={Login2}/>
    <Route path='/Login3' component={Login3}/>
    <Route path='/Trial' component={Trial}/>
    </Switch>
    </Router>
    );
  };
}


export default App;