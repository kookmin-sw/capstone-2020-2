import React, { Component } from 'react';
import '../App.css';
import LoginAlert from '../components/loginSuccessAlert';
import { Button, Grid, withStyles, Typography } from '@material-ui/core/';
import {
  Link,
  withRouter,
  BrowserRouter as Router,
  Route,
  Switch,
} from 'react-router-dom';
import UserContext from '../UserContext';

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
  state = {
    close: true,
  };

  static contextType = UserContext;
  render() {
    const { classes } = this.props;
    const { user } = this.context;
    console.log(user);

    return (
      <div class="container-fluid">
        <LoginAlert userName={user.name}></LoginAlert>
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
export default withRouter(withStyles(style)(Option));
