import React from 'react';

class NewGame extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            numberOfRounds: '',
        }
        
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        this.setState({numberOfRounds: event.target.value});
    }

    handleSubmit(event) {
        alert('Number of rounds: ' + this.state.numberOfRounds);
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

export default NewGame;