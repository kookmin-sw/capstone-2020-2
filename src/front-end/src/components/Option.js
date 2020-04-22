import React, {Component} from "react";
import "../App.css";
// import {Spinner, Button, Label} from "reactstrap";
import {Button, Grid, withStyles, Typography,IconButton} from '@material-ui/core/';
import {Alert,AlertTitle} from '@material-ui/lab/';
import CloseIcon from '@material-ui/icons/Close';

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
      close : true
		};
  }
 

	render() {
    const { classes } = this.props;
    


		return (
			<div class="container-fluid">
        <Alert severity="info"action ={ <IconButton
              aria-label="close"
              color="inherit"
              size="small"
              onClick={() => {
                this.setState({close:false });
              }}
            >
              <CloseIcon fontSize="inherit" />
            </IconButton>}>
          <AlertTitle>Login!</AlertTitle>
          로그인 되었습니다. - <strong></strong>
        </Alert>
          <Grid container spacing={10} direction="row" justify="center" alignItems="center" style={{height: '900px'}}>
            <Grid item>
              <Link to = "/VideoPlay">
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
