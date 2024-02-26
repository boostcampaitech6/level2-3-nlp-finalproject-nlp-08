import React from 'react';
import { useLocation } from 'react-router-dom';
import FixedTextBox from '../components/FixedTextBox';

const ResultPage = () => {
  const location = useLocation();
  const text = location.state.text;

  return (
    <div>
      <h1>문제 풀어보기</h1>
      <div>
        <FixedTextBox value={text} />
      </div>
      {/* Add your content here */}
    </div>
  );
};

export default ResultPage;