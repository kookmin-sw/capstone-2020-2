import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';
import 'bootstrap/dist/css/bootstrap.css'


ReactDOM.render(<App />, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();

<<<<<<< HEAD
export { default as Login } from './components/Main';

=======
export { default as Main } from './components/Main';
>>>>>>> fb903e8c7c8d28dc16df70cad12bbced2def76d9
