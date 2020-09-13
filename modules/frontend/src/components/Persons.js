import React, { Component } from 'react';
import Connection from './Connection';
import './Persons.css';

class Persons extends Component {
  constructor(props) {
    super(props);
    // TODO: endpoint should be abstracted into a config variable
    this.endpoint_url = 'http://localhost:30001/api/persons';
    this.state = {
      persons: [],
      display: null,
    };
  }

  componentDidMount() {
    	fetch(this.endpoint_url)
      .then((response) => response.json())
      .then((data) => this.setState({ persons: data }));
  }

	setDisplay = (personId) => {
    	this.setState({
	    persons: this.state.persons,
	    display: personId,
	  });
	}

	render() {
	  return (
  <div>
    <ul>
      {this.state.persons.map((person) => (
        <li key={person.id}>
          <div className="person" onClick={() => { this.setDisplay(person.id); }}>
            {person.first_name}
            {' '}
            {person.last_name}
          </div>
          <div>
            Company:
            {person.company_name}
            
          </div>
        </li>
      ))}
    </ul>
    <Connection personId={this.state.display} />
  </div>
	  );
	}
}
export default Persons;
