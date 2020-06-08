import React, { Component } from 'react';
import axios from 'axios';
import '../App.css';
import {
  Link,
  BrowserRouter as Router,
  withRouter,
  Route,
  Switch,
} from 'react-router-dom';
import {
  Grid,
  Button,
  Input,
  TextField,
  InputAdornment,
  Typography,
} from '@material-ui/core';
import { PieChart, Pie, Sector, Cell } from 'recharts';
import UserContext from '../UserContext';
import NavBar from '../components/NavBar';

const COLORS = ['#ffcc5c', '#87bdd8', '#96ceb4', '#6b5b95', '#e6e2d3'];

const renderActiveShape = (props) => {
  const RADIAN = Math.PI / 180;
  const {
    cx,
    cy,
    midAngle,
    innerRadius,
    outerRadius,
    startAngle,
    endAngle,
    fill,
    payload,
    percent,
    multi,
  } = props;
  const sin = Math.sin(-RADIAN * midAngle);
  const cos = Math.cos(-RADIAN * midAngle);
  const sx = cx + (outerRadius + 10) * cos;
  const sy = cy + (outerRadius + 10) * sin;
  const mx = cx + (outerRadius + 30) * cos;
  const my = cy + (outerRadius + 30) * sin;
  const ex = mx + (cos >= 0 ? 1 : -1) * 22;
  const ey = my;
  const textAnchor = cos >= 0 ? 'start' : 'end';

  return (
    <g>
      <text
        font-size="30px"
        x={cx}
        y={cy}
        dy={8}
        textAnchor="middle"
        fill={fill}
      >
        {payload.emotionTag}
      </text>
      <Sector
        cx={cx}
        cy={cy}
        innerRadius={innerRadius}
        outerRadius={outerRadius}
        startAngle={startAngle}
        endAngle={endAngle}
        fill={fill}
      />
      <Sector
        cx={cx}
        cy={cy}
        startAngle={startAngle}
        endAngle={endAngle}
        innerRadius={outerRadius + 6}
        outerRadius={outerRadius + 10}
        fill={fill}
      />
      <path
        d={`M${sx},${sy}L${mx},${my}L${ex},${ey}`}
        stroke={fill}
        fill="none"
      />
      <circle cx={ex} cy={ey} r={2} fill={fill} stroke="none" />
      <text
        x={ex + (cos >= 0 ? 1 : -1) * 12}
        y={ey}
        textAnchor={textAnchor}
        fill="#333"
      >
        {`${multi}`}{' '}
      </text>
      <text
        x={ex + (cos >= 0 ? 1 : -1) * 12}
        y={ey}
        dy={18}
        textAnchor={textAnchor}
        fill="#999"
      >
        {`(${percent * 100}%)`}
      </text>
    </g>
  );
};

class Result extends Component {
  constructor(props) {
    super(props);
    this.state = {
      signalData: [
        {
          emotionTag: 'happiness',
          multi: 0.2,
          face: 0.1,
          eeg: 0.3,
          fullMark: 1.0,
        },
        {
          emotionTag: 'sadness',
          multi: 0.2,
          face: 0.2,
          eeg: 0.2,
          fullMark: 1.0,
        },
        {
          emotionTag: 'disgust',
          multi: 0.3,
          face: 0.7,
          eeg: 0.5,
          fullMark: 1.0,
        },
        {
          emotionTag: 'fear',
          multi: 0.1,
          face: 0.0,
          eeg: 0.0,
          fullMark: 1.0,
        },
        {
          emotionTag: 'neutral',
          multi: 0.2,
          face: 0.0,
          eeg: 0.0,
          fullMark: 1.0,
        },
      ],

      user: {
        id: 0,
        name: '',
        loggedIn: false,
      },
      emotionTag: null,
      imageIndex: 1,
      activeIndex: 0,
    };
  }

  static contextType = UserContext;
  onPieEnter = (data, index) => {
    this.setState({
      activeIndex: index,
    });
  };

  getFinalData = () => {
    axios
      .get(`api/v1/analyze/final-result/`, {
        // headers: {
        //   'content-type': 'multipart/form-data',
        // },
      })
      .then((response) => {
        if (response.data.multiResult) {
          let newSignalData = [];
          const emotionList = [
            'happiness',
            'sadness',
            'disgust',
            'fear',
            'neutral',
          ];
          for (let emotionIdx = 0; emotionIdx < 5; emotionIdx++) {
            newSignalData.push({
              emotionTag: emotionList[emotionIdx],
              multi: response.data.multiResult[emotionList[emotionIdx]],
              face: response.data.faceResult[emotionList[emotionIdx]],
              eeg: response.data.eegResult[emotionList[emotionIdx]],
              fullMark: 1.0,
            });
          }
          this.setState({
            signalData: newSignalData,
            hasAnalyzeData: true,
          });
        }
      });
  };

  render() {
    const { user } = this.context;
    return (
      <div class="full-container">
        {!this.state.hasAnalyzeData ? (
          this.getFinalData()
        ) : (
          <div>
            <NavBar />
            <Grid container id="loginBox" direction="column" justify="center">
              <Typography variant="h3" id="resultText">
                {user.name}님의 최종감정입니다.
              </Typography>
              <PieChart width={400} height={400} class="Pie" id="PieEEG">
                <Pie
                  name="emotionTag"
                  data={this.state.signalData}
                  cx={250}
                  cy={300}
                  startAngle={180}
                  endAngle={0}
                  outerRadius={110}
                  fill="#ffc2c2"
                  dataKey="face"
                  label
                >
                  {this.state.signalData.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={COLORS[index % COLORS.length]}
                    />
                  ))}
                </Pie>
              </PieChart>
              <PieChart width={600} height={600} class="Pie" id="PieMulti">
                <Pie
                  data={this.state.signalData}
                  activeIndex={this.state.activeIndex}
                  activeShape={renderActiveShape}
                  cx={300}
                  cy={300}
                  innerRadius={110}
                  outerRadius={180}
                  fill="#554475"
                  dataKey="multi"
                  labelLine={false}
                  onMouseEnter={this.onPieEnter}
                >
                  {this.state.signalData.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={COLORS[index % COLORS.length]}
                    />
                  ))}
                </Pie>
              </PieChart>
              <PieChart width={400} height={400} class="Pie" id="PieFace">
                <Pie
                  data={this.state.signalData}
                  cx={200}
                  cy={300}
                  startAngle={180}
                  endAngle={0}
                  outerRadius={110}
                  fill="#86c1e0"
                  dataKey="eeg"
                  label
                >
                  {this.state.signalData.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={COLORS[index % COLORS.length]}
                    />
                  ))}
                </Pie>
              </PieChart>
            </Grid>
          </div>
        )}
      </div>
    );
  }
}

export default withRouter(Result);
