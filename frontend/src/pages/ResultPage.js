import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import FixedTextBox from '../components/FixedTextBox';
import NormalButton from '../components/NormalButton';
import QuestionBox from '../components/QuestionBox';
import CheckAnswerBox from '../components/CheckAnswerBox';
import './ResultPage.css';


const ResultPage = () => {
  const location = useLocation();
  console.log("Location state:", location.state);
  const text = location.state.text;
  const question = location.state.question;
  const correctAnswer = location.state.answer;
  console.log("Text:", text);
  console.log("Question:", question);
  console.log("Correct Answer:", correctAnswer);
  const [userAnswer, setUserAnswer] = useState("");
  const [isAnswerCorrect, setIsAnswerCorrect] = useState(false);
  const [buttonClicked, setButtonClicked] = useState(false);

  const handleCheckAnswer = () => {
    setIsAnswerCorrect(userAnswer === correctAnswer);
    setButtonClicked(true);
  };

  return (
    <div>
      <h1>문제 풀어보기</h1>
      <div className='result-area' >
        <FixedTextBox value={text} />
        <div className='answer-input'>
          <QuestionBox value={question} />
          <input
            className='input'
            type='text'
            placeholder='답을 입력하세요.'
            value={userAnswer}
            onChange={(e) => setUserAnswer(e.target.value)}
          />
          {buttonClicked && (
            <CheckAnswerBox isAnswerCorrect={isAnswerCorrect} correctAnswer={correctAnswer} />
          )}
        </div>
        
      </div>
      
      <div className='back-button-container'>
        <NormalButton label="채점하기" onClick={handleCheckAnswer}/>
        <NormalButton label="돌아가기" onClick={() => window.history.back()} />
      </div>
    </div>
  );
};

export default ResultPage;