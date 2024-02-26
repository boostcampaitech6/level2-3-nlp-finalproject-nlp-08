// HomePage.js

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import NormalButton from '../components/NormalButton';
import InputTextBox from '../components/InputTextBox';
import toast, { Toaster } from 'react-hot-toast';

function HomePage() {
  console.log('HomePage component rendered');

  const [text, setText] = useState("");
  const navigate = useNavigate();

  const handleSendTextClick = () => {
    if (text.length < 10) {
        toast.error('10자 이상 입력해주세요.');
        return;
    } else {}
        navigate('/result', { state: { text: text } });
  };

  const handleDeleteTextClick = () => {
    setText('');
  };

  return (
    <div className="App">
      <div className='box-description'>
        <p>분석하고 싶은 글을 입력해주세요</p>
      </div>

      <InputTextBox value={text} onChange={(e) => setText(e.target.value)} />

      <div className="mainpage-button-container">
        <NormalButton label="분석하기" onClick={ handleSendTextClick } />
        <NormalButton label="전체 삭제" onClick={ handleDeleteTextClick } />
        <Toaster
          position="top-right"
          reverseOrder={false}
        />
      </div>
    </div>
  );
}

export default HomePage;
