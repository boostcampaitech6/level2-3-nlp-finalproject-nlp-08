import React from 'react';
import { useLocation } from 'react-router-dom';

const ResultPage = () => {
  const location = useLocation();
  const text = location.state.text;

  return (
    <div>
      <h1>Result Page</h1>
      <p>본문 내용: {text}</p>
      {/* Add your content here */}
    </div>
  );
};

export default ResultPage;