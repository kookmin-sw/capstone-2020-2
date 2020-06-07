import React, { Component } from 'react';
import '../App.css';
import {
  Button,
  Card,
  CardContent,
  Grid,
  Hidden,
  Typography,
} from '@material-ui/core';

class IntroCard extends Component {
  render() {
    return (
      <Card id="startCard">
        <CardContent
          style={{
            height: '100%',
            paddingTop: '8%',
            textAlign: 'center',
          }}
        >
          <Grid
            item
            style={{
              marginBottom: '10%',
            }}
          >
            <Typography
              variant="h4"
              style={{
                marginBottom: '5%',
              }}
            >
              Get started!
            </Typography>{' '}
            <Hidden smDown>
              <Typography variant="subtitle1">
                이 곳에 당신의 얼굴을 보여주세요. <br />
                EEG와 표정을 이용한 감정인식이 가능합니다.{' '}
              </Typography>{' '}
            </Hidden>{' '}
          </Grid>{' '}
          <Grid item>
            <Hidden smDown>
              <hr />
              <Typography
                variant="caption"
                style={{
                  marginTop: '10%',
                }}
              >
                * 수집된 데이터는 삭제되지 않습니다.{' '}
              </Typography>{' '}
            </Hidden>{' '}
            <Button
              color="primary"
              variant="outlined"
              href="/Login"
              id="startCardBtn"
              style={{
                margin: '5%',
              }}
            >
              start{' '}
            </Button>{' '}
          </Grid>{' '}
        </CardContent>{' '}
      </Card>
    );
  }
}

export default IntroCard;
