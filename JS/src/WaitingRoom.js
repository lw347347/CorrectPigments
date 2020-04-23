import React from 'react';
import { withRouter } from 'react-router-dom';
import PropTypes from 'prop-types';

class WaitingRoom extends React.Component {
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

    handleSubmit(event) {
        // Call the api
        // const response = await axios.get('http://localhost:8000/CreateGame/' + this.state.numberOfRounds)

        // 
        event.preventDefault();
    }
  
    render() {
        const { match, location, history } = this.props
        return (
            <div>
                Your game code is {location.state.gameCode}.
            </div>
        )
    }
    
}

export default withRouter(WaitingRoom);