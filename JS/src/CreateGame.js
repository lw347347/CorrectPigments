import React from 'react';
import WaitingRoom from './WaitingRoom';
import axios from 'axios';
import { useHistory } from "react-router-dom";

function withMyHook(Component) {
    return function WrappedComponent(props) {
        const myHookValue = useHistory();
        return <CreateGame {...props} history={myHookValue} />;
    }
}

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

    async handleSubmit(event) {
        // Prevent the page from reloading
        event.preventDefault();

        // Call the api
        const response = await axios.get('http://localhost:8000/CreateGame/' + this.state.numberOfRounds)

        // Send them to the waiting room
        this.props.history.push({
            pathname: '/WaitingRoom',
            state: { gameCode: response.data }
        });  
    }
  
    render() {
        return (
            <div>
                <h1>New Game</h1>
                <form onSubmit={this.handleSubmit}>
                    <label>
                    How many rounds? {this.state.gameCode}
                    <input type="text" value={this.state.numberOfRounds} onChange={this.handleChange} />
                    </label>
                    <input type="submit" value="Submit" />
                </form>
            </div>
        )
    }
    
}

export default withMyHook(CreateGame);