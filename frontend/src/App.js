import React from 'react';
import './App.css';

function App() {
  return (
    <div className="App">
      {/* 중앙 텍스트 박스 */}
      <div className="center-container">  
        <textarea
          className="large-input"
          placeholder="Type your text here..."
        />
      </div>
    </div>
  );
}

export default App;