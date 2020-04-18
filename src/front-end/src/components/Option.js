import React, {Component} from "react";
import Webcam from "react-webcam";
import "../App.css";
// import {Spinner, Button, Label} from "reactstrap";
import Button from "@material-ui/core/Button";
import {Link, BrowserRouter as Router, Route, Switch} from "react-router-dom";

class Option extends Component {
  constructor(props) {
		super(props);
		this.state = {
		};
	}

	render() {
		return (
			<div class="container-fluid">
				<div class="row">
					<div class="col-4" id="option">
					     <Button color="primary" style={{margin: "20%"}}>체험
               </Button>
					</div>
          <div class="col-4" id="option">
               <Button color="primary">분석
               </Button>
          </div>
				</div>
			</div>
		);
	}
}

export default Option;
