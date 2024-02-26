import React from 'react';
import { useLocation } from 'react-router-dom';
import FixedTextBox from '../components/FixedTextBox';
import NormalButton from '../components/NormalButton';

const ResultPage = () => {
  const location = useLocation();
  const text = location.state.text;

  return (
    <div>
      <h1>문제 풀어보기</h1>
      <div>
        <FixedTextBox value={text} />
      </div>
      
      <div className='back-button-container'>
        <NormalButton label="돌아가기" onClick={() => window.history.back()} />
      </div>
    </div>
  );
};

export default ResultPage;