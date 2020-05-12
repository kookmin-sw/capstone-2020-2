import React, { Component } from 'react';
import '../App.css';
import { IconButton } from '@material-ui/core';
import { Alert, AlertTitle } from '@material-ui/lab/';
import Collapse from '@material-ui/core/Collapse';
import CloseIcon from '@material-ui/icons/Close';

class LoginSuccessAlert extends Component {
  constructor(props) {
    super(props);
    this.state = {
      close: true,
    };
  }

  render() {
    return (
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
          <AlertTitle> Login! </AlertTitle>
          {this.props.userName}님 안녕하세요!
          <strong> </strong>
        </Alert>
      </Collapse>
    );
  }
}

export default LoginSuccessAlert;
