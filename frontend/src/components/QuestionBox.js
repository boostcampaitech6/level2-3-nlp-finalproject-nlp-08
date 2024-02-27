import React from 'react';
import './QuestionBox.css';

const QuestionBox = ({ value }) => {

  return (
    <div className="right-container">
      <p>
        {value}
      </p>
    </div> 
  );
};

export default QuestionBox;