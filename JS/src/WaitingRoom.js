import React from 'react';

class WaitingRoom extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            gameCode: props.gameCode,
        }
        
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        this.setState({numberOfRounds: event.target.value});
    }

    handleSubmit(event) {
        // Call the api
        // const response = await axios.get('http://localhost:8000/CreateGame/' + this.state.numberOfRounds)

        // 
        event.preventDefault();
    }
  
    render() {
        return (
            <div>
                Your game code is {this.state.gameCode}.
            </div>
        )
    }
    
}

export default WaitingRoom;