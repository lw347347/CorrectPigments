import React from 'react';

class JoinGame extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            gameID: '',
            firstName: '',
            nickname: '',
        }

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        this.setState({
            [event.target.name]: event.target.value
        });
    }

    handleSubmit(event) {
        // Call the API
        event.preventDefault();
    }
  
    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <label>
                    Game ID:
                </label>
                <input type="text" name='gameID' value={this.state.gameID} onChange={this.handleChange} />
                <label>
                    First Name
                </label>
                <input type="text" name='firstName' value={this.state.firstName} onChange={this.handleChange} />
                <label>
                    Nickname
                </label>
                <input type="text" name='nickname' value={this.state.nickname} onChange={this.handleChange} />
                <input type="submit" value="Submit" />
            </form>
        )
    }
    
}

export default JoinGame;