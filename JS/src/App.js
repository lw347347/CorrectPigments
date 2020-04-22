import React from 'react';
import './App.css';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
import { Navbar, Nav } from 'react-bootstrap';
import NewGame from './NewGame';
import JoinGame from './JoinGame';

function App(props) {
  return (    
    <div className="App">
      <Router>
        <Navbar expand="lg">
          <Nav.Link><Link to="/JoinGame">Home</Link></Nav.Link>
          <Nav.Link><Link to="/NewGame">New Game</Link></Nav.Link>
        </Navbar>
        <Switch>
          <Route path="/JoinGame">
            <JoinGame />
          </Route>
          <Route path="/NewGame">
            <NewGame />
          </Route>
          <Route path="/">
            <JoinGame />
          </Route>
        </Switch>
      </Router>
    </div> 
  );
}

export default App;
