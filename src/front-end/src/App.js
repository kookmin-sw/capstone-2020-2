import React, {Component} from "react";

import Login from "./components/Login";
import Main from "./components/Main";
import Signup from "./components/Signup";
import Option from "./components/Option";
import VideoPlay from "./components/VideoPlay"


import "./App.css";
import axios from "axios";
import {Link, BrowserRouter as Router, Route, Switch} from "react-router-dom";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

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
<<<<<<< HEAD
					<Route path="/VideoPlay" component={VideoPlay} />
=======
          			<Route path="/Option" component={Option} />
					<Route path="/VideoPlay" component={VideoPlay} />
					<Router path="/Analyze" component={Analyze} />
>>>>>>> fb903e8c7c8d28dc16df70cad12bbced2def76d9
				</Switch>
			</Router>
		);
	}
}

export default App;
