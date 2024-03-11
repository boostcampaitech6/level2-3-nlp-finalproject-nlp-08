import React from 'react';
import './QuestionBox.css';
import { FaCheckCircle, FaQuestionCircle,  } from "react-icons/fa";
import { FaCircleXmark } from "react-icons/fa6";

const QuestionBox = ({ value , isCorrect, isAllCorrect }) => {
  const getClassName = () => {
    if (isCorrect === true || isAllCorrect === true) {
      return 'correct';
    } else if (isCorrect === false) {
      return 'incorrect shake';
    }
    return '';
  };

  const className = getClassName();
  const text = isAllCorrect ? '모든 문제를 맞추셨습니다!' : value;

  return (
    <div className={`right-container {$className}`}>
      <textarea className={`large-right-textbox ${className}`} disabled={true} value={text} readOnly/>
      {isAllCorrect === false && isCorrect === true && <FaCheckCircle className="checking-icon correct" />}
      {isAllCorrect === false && isCorrect === false && <FaCircleXmark className="checking-icon incorrect" />}
      {isAllCorrect === false && isCorrect === null && <FaQuestionCircle className="checking-icon" />}
    </div> 
  );
};

export default QuestionBox;