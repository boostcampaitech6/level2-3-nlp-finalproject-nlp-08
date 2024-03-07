import React from 'react';
import './QuestionBox.css';
import { FaCheckCircle, FaQuestionCircle,  } from "react-icons/fa";
import { FaCircleXmark } from "react-icons/fa6";

const QuestionBox = ({ value , isCorrect}) => {

  return (
    <div className="right-container">
      <textarea className="large-right-textbox" disabled={true} value={value} readOnly/>
      {isCorrect === true && <FaCheckCircle className="checking-icon correct" />}
      {isCorrect === false && <FaCircleXmark className="checking-icon incorrect" />}
      {isCorrect === null && <FaQuestionCircle className="checking-icon" />}
    </div> 
  );
};

export default QuestionBox;