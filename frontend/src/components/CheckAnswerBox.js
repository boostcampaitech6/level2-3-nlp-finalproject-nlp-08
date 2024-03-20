import React from 'react';
import './CheckAnswerBox.css';

const CheckAnswerBox = ({ isAnswerCorrect, correctAnswer }) => {

  const correctMessage = '정답입니다.';
  const wrongMessage = `오답입니다. 정답은 `+ correctAnswer+ `입니다.`;

  return (
    <div className='result-message-container'>
      <p>
        {isAnswerCorrect ? correctMessage : wrongMessage}
      </p>
    </div>
  );
};

export default CheckAnswerBox;