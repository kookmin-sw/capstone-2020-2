import React, { Component } from 'react';
import '../App.css';
// import {Spinner, Button, Label} from "reactstrap";
import {
  Button,
  Grid,
  withStyles,
  Typography,
  IconButton,
} from '@material-ui/core/';
import { Alert, AlertTitle } from '@material-ui/lab/';
import Collapse from '@material-ui/core/Collapse';
import CloseIcon from '@material-ui/icons/Close';

// import Button from "@material-ui/core/Button";
// import Grid from '@material-ui/core/Grid';
import { Link, BrowserRouter as Router, Route, Switch } from 'react-router-dom';

const style = {
  btnStyle: {
    textAlign: 'center',
    maxWidth: '250px',
    maxHeight: '200px',
    minWidth: '250px',
    minHeight: '200px',
  },
};

class Option extends Component {
  constructor(props) {
    super(props);
    this.state = {
      close: true,
    };
  }

  render() {
    const { classes } = this.props;

    return (
      <div class="container-fluid">
        <Collapse in={this.state.close}>
          <Alert
            severity="info"
            action={
              <IconButton
                aria-label="close"
                color="inherit"
                size="small"
                onClick={() => {
                  this.setState({
                    close: false,
                  });
                }}
              >
                <CloseIcon fontSize="inherit" />
              </IconButton>
            }
          >
            <AlertTitle> Login! </AlertTitle>{' '}
            {this.props.location.state.userName}님 안녕하세요!{' '}
            <strong> </strong>{' '}
          </Alert>{' '}
        </Collapse>{' '}
        <Grid
          container
          spacing={10}
          direction="row"
          justify="center"
          alignItems="center"
          style={{
            height: '900px',
          }}
        >
          <Grid item>
            <Link to="/Trial">
              <Button
                className={classes.btnStyle}
                color="primary"
                variant="contained"
              >
                <Typography variant="h5"> 체험 </Typography>{' '}
              </Button>{' '}
            </Link>{' '}
          </Grid>{' '}
          <Grid item>
            <Link to="/Analyze">
              <Button
                className={classes.btnStyle}
                color="primary"
                variant="contained"
              >
                <Typography variant="h5"> 분석 </Typography>{' '}
              </Button>{' '}
            </Link>{' '}
          </Grid>{' '}
        </Grid>{' '}
      </div>
    );
  }
}

Option.propTypes = {};
export default withStyles(style)(Option);
