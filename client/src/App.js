import React, { Component } from 'react';
import './App.css';
import TextEditor from './components/TextEditor/TextEditor';

class App extends Component {
  render() {
    return (
      <div className="App">
        <TextEditor />
      </div>
    );
  }
}

export default App;
