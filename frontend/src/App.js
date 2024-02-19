/* eslint-disable*/

import React, { useState } from 'react';
import './App.css';
import NormalButton from './components/NormalButton';
import InputTextBox from './components/InputTextBox';

function App() {
  const [text, setText] = useState('');

  return (
    <div className="App">
      {/* Description text */}
      <div className='box-description'>
        <p>분석하고 싶은 글을 입력해주세요</p>
      </div>

      {/* 중앙 텍스트 박스 */}
      <InputTextBox value={text} onChange={(e) => setText(e.target.value)} />

      {/* 버튼 */}
      <div className="mainpage-button-container">
          <NormalButton label="분석하기" onClick={() => console.log('Button 1 clicked')} />
          <NormalButton label="전체 삭제" onClick={() => console.log('Button 2 clicked')} />
        </div>
    </div>
  );
}

export default App;