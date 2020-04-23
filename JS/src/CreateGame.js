import React from 'react';
import WaitingRoom from './WaitingRoom';
import axios from 'axios'

class CreateGame extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            numberOfRounds: '',
            gameCode: '',
        }
        
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        this.setState({numberOfRounds: event.target.value});
    }

    handleSubmit(event) {
        // Call the api
        const response = axios.get('http://localhost:8000/CreateGame/' + this.state.numberOfRounds)

        this.setState({ gameCode: response})
        console.log(this.state.gameCode) 

        // // Call the waiting room
        // <WaitingRoom >
        

        event.preventDefault();
    }
  
    render() {
        return (
            <div>
                <h1></h1>New Game
                <form onSubmit={this.handleSubmit}>
                    <label>
                    How many rounds?
                    <input type="text" value={this.state.numberOfRounds} onChange={this.handleChange} />
                    </label>
                    <input type="submit" value="Submit" />
                </form>
            </div>
        )
    }
    
}

export default CreateGame;