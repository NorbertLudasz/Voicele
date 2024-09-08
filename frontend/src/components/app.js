import React, { Component } from 'react';
import { render } from 'react-dom';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
//import Navbar from './navbar';
import HomePage from './homepage';
import StatsPage from './statspage';
import PastGames from './pastgames';
import CreateGamePage from './creategamepage';
import RegisterPage from './registerpage';
import LoginPage from './loginpage';
import GamePage from './gamepage';
import '../../static/css/navbar.css';

export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoggedIn: false,
      username: '',
    };
  }

  render() {
    return (
      <Router>
        <div>
          <div className="page-content">
            <Routes>
              <Route path='/' element={<HomePage />} />
              <Route path='/stats' element={<StatsPage />} />
              <Route path='/pastgames' element={<PastGames />} />
              <Route path='/creategame' element={<CreateGamePage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/play/:id" element={<GamePage />} />
            </Routes>
          </div>
        </div>
      </Router>
    );
  }
}

const appDiv = document.getElementById("app");
render(<App />, appDiv);