import React from 'react';
import './App.css';

function App() {
  return (
    <div className="App">
      {/* Description text */}
      <div className='box-description'>
        <p>분석하고 싶은 글을 입력해주세요</p>
      </div>

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