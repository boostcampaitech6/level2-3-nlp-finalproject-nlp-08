import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import FixedTextBox from '../components/FixedTextBox';
import NormalButton from '../components/NormalButton';
import QuestionBox from '../components/QuestionBox';
import CheckAnswerBox from '../components/CheckAnswerBox';
import './ResultPage.css';


const ResultPage = () => {
  const location = useLocation();
  const text = location.state.text;
  const [question, setQuestion] = useState("");
  const [userAnswer, setUserAnswer] = useState("");
  const [correctAnswer, setCorrectAnswer] = useState("");
  const [isAnswerCorrect, setIsAnswerCorrect] = useState(false);
  const [buttonClicked, setButtonClicked] = useState(false);

  useEffect(() => {
    axios.get('http://localhost:8000/text')
      .then(response => {
        setQuestion(response.data.question);
        setCorrectAnswer(response.data.answer);
      })
      .catch(error => {
        console.error('Error fetching question:', error);
      });
  }, []);

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