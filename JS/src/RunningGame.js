import React from 'react';
import { withRouter } from 'react-router-dom';
import PropTypes from 'prop-types';
import axios from 'axios';

class RunningGame extends React.Component {
    static propTypes = {
        match: PropTypes.object.isRequired,
        location: PropTypes.object.isRequired,
        history: PropTypes.object.isRequired
    }

    constructor(props) {
        super(props);
        this.state = {
            gameCode: props.location.state.gameCode,
        }
        
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        this.setState({numberOfRounds: event.target.value});
    }

    async handleSubmit(event) {
        // Prevent the page from reloading
        event.preventDefault();

        console.log(this.state.gameCode)

        // Call the api
        const response = await axios.get('http://localhost:8000/StartGame/' + this.state.gameCode)

        // Send them to the score board
        this.props.history.push({
            pathname: '/RunningGame',
            state: { gameCode: response.data }
        });  
    }
  
    render() {
        const { match, location, history } = this.props
        return (
            <div>
                Your game code is {location.state.gameCode}.
                <button onClick={this.handleSubmit}>Start Game</button>
            </div>
        )
    }
    
}

export default withRouter(RunningGame);