import React, { Component } from 'react';

const UserContext = React.createContext({
  user: { id: '', name: '', loggedIn: false },
});

class UserProvider extends Component {
  // Context state
  state = {
    user: '',
    setUser: this.setUser.bind(this),
    unsetUser: this.unsetUser.bind(this),
  };

  // Method to update state
  setUser(newUser) {
    // console.log('hihihi setUser');
    this.setState({ user: newUser });
    console.log('hey setUser success');
  }

  unsetUser() {
    this.setState({ user: { id: 0, name: '', loggedIn: false } });
  }

  render() {
    const { children } = this.props;
    return (
      <UserContext.Provider value={this.state}>{children}</UserContext.Provider>
    );
  }
}

export { UserProvider };
export const UserConsumer = UserContext.Consumer;
export default UserContext;
