import React, { Component } from "react";
import Connection from "./Connection";

class Persons extends Component {
  constructor(props) {
    super(props);
    // TODO: endpoint should be abstracted into a config variable
    this.endpoint_url = "http://localhost:30001/api/persons";
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
  };

  render() {
    return (
      <div className="lists">
        <div className="peopleBox">
          <div className="peopleHeader">People</div>
          <ul className="personList">
            {this.state.persons.map((person) => (
              <li
                key={person.id}
                onClick={() => {
                  this.setDisplay(person.id);
                }}
                className={
                  this.state.display === person.id
                    ? "selectedPerson"
                    : "personListItem"
                }
              >
                <div className="person">
                  {person.first_name} {person.last_name}
                </div>
                <div>
                  Company: <strong>{person.company_name}</strong>{" "}
                </div>
              </li>
            ))}
          </ul>
        </div>
        <Connection personId={this.state.display} />
      </div>
    );
  }
}
export default Persons;
