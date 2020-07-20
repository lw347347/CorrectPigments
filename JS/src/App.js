import React from 'react';
import './App.css';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
import { Navbar, Nav } from 'react-bootstrap';
import CreateGame from './CreateGame';
import JoinGame from './JoinGame';
import WaitingRoom from './WaitingRoom';

function App(props) {
  return (    
    <div className="App">
      <Router>
        <Navbar expand="lg">
          <Nav.Link><Link to="/JoinGame">Home</Link></Nav.Link>
          <Nav.Link><Link to="/CreateGame">Create Game</Link></Nav.Link>
        </Navbar>
        <Switch>
          <Route path="/JoinGame">
            <JoinGame />
          </Route>
          <Route path="/CreateGame">
            <CreateGame />
          </Route>
          <Route path="/WaitingRoom">
            <WaitingRoom />
          </Route>
          <Route path="/">
            <CreateGame />
          </Route>
        </Switch>
      </Router>
    </div> 
  );
}

export default App;
