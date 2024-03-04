import React from 'react';
import './QuestionBox.css';

const QuestionBox = ({ value }) => {

  return (
    <div className="right-container">
      <textarea className="large-right-textbox" disabled={true} value={value} readOnly/>
    </div> 
  );
};

export default QuestionBox;