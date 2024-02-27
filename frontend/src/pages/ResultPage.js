import React from 'react';
import { useLocation } from 'react-router-dom';
import FixedTextBox from '../components/FixedTextBox';
import NormalButton from '../components/NormalButton';
import QuestionBox from '../components/QuestionBox';
import './ResultPage.css';

const ResultPage = () => {
  const location = useLocation();
  const text = location.state.text;
  const question = "이것이 문제의 내용이다. 이것이 문제의 내용이다. 이것이 문제의 내용이다. 이것이 문제의 내용이다. 이것이 문제의 내용이다. 이것이 문제의 내용이다. 이것이 문제의 내용이다. 이것이 문제의 내용이다. 이것이 문제의 내용이다. 이것이 문제의 내용이다. 이것이 문제의 내용이다. 이것이 문제의 내용이다. 이것이 문제의 내용이다. 이것이 문제의 내용이다. 이것은 무엇인가?"
  const answerinput = "답: "

  return (
    <div>
      <h1>문제 풀어보기</h1>
      <div className='result-area' >
        <FixedTextBox value={text} />
        <div className='answer-input'>
          <QuestionBox value={question} />
          <input className='input' type='text' placeholder={answerinput} />
        </div>
      </div>
      
      
      <div className='back-button-container'>
        <NormalButton label="채점하기" onClick={() => window.history.back()} />
        <NormalButton label="돌아가기" onClick={() => window.history.back()} />
      </div>
    </div>
  );
};

export default ResultPage;