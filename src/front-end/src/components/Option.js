import React, {Component} from "react";
import Webcam from "react-webcam";
import "../App.css";
// import {Spinner, Button, Label} from "reactstrap";
import {Button, Grid, withStyles, Typography} from '@material-ui/core/';
// import Button from "@material-ui/core/Button";
// import Grid from '@material-ui/core/Grid';
import {Link, BrowserRouter as Router, Route, Switch} from "react-router-dom";

const style = {
  btnStyle: {
    textAlign: 'center',
    maxWidth: '250px',
    maxHeight: '200px',
    minWidth: '250px',
    minHeight: '200px'
  },
};

class Option extends Component {
  constructor(props) {
		super(props);
		this.state = {
		};
  }
  
	render() {
    const { classes } = this.props;
		return (
			<div class="container-fluid">
          <Grid container spacing={10} direction="row" justify="center" alignItems="center" style={{height: '900px'}}>
            <Grid item>
              <Link to = "/Trial">
              <Button className={classes.btnStyle} color="primary" variant="contained" ><Typography variant="h5">체험</Typography></Button>
              </Link>
            </Grid>
            <Grid item>
              <Link to = "/Analyze">
                <Button className={classes.btnStyle} color="primary" variant="contained"><Typography variant="h5">분석</Typography></Button>
              </Link>
            </Grid>
          </Grid>
			</div>
		);
	}
}


Option.propTypes = {};
export default withStyles(style)(Option);
