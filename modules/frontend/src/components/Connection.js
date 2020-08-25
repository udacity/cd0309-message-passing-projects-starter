import React, { Component } from 'react';

class Connection extends Component {
  constructor(props) {
    super(props);

    this.state = {
      connections: [],
      personId: null,
    };
  }

  componentDidUpdate() {
    const { personId } = this.props;
    if (Number(personId) !== Number(this.state.personId)) {
      this.setState({ personId, connections: this.state.connections });
      this.getConnections(personId);
    }
  }

    getConnections = (personId) => {
      if (personId) {
        // TODO: endpoint should be abstracted into a config variable
        fetch(`http://localhost:30001/api/connections/persons/${personId}/connection?start_date=2020-01-01&end_date=2020-12-30&distance=5`)
          .then((response) => response.json())
          .then((connections) => this.setState({ connections: connections, personId: this.state.personId }));
      }
    };

    render() {
      return (
        <div>
          <h3>Connections</h3>
          <ul>
            {this.state.connections.map((connection) => (
              <div>
                <li>
                  <h4>
                    {connection.person.first_name}
                    {' '}
                    {connection.person.last_name}
                  </h4>
                  (
                  {connection.location.latitude}
                  ,
                  {connection.location.longitude}
                  ) at
                  {connection.location.creation_time}
                </li>
              </div>

            ))}
          </ul>
        </div>
      );
    }
}
export default Connection;
