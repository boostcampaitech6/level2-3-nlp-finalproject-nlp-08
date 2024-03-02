import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast, { Toaster } from 'react-hot-toast';
import axios from 'axios';

import NormalButton from '../components/NormalButton';
import InputTextBox from '../components/InputTextBox';
import './HomePage.css';

function HomePage() {
  const [text, setText] = useState("");
  const navigate = useNavigate();
  const sample_answers = ["2013년 9월"]
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/generate';
  const MIN_TEXT_LENGTH = 10;


  const handleSendTextClick = () => {
    if (text.length < MIN_TEXT_LENGTH) {
        toast.error('10자 이상 입력해주세요.');
        return;
    }

    axios.post(API_URL, { 
      context: text,
      answers: sample_answers
    })
    .then((response) => {
      const result_doc  = response.data;
      const questionAnswerPairs = result_doc.question_answer_pairs;

      console.log(result_doc);
      let firstQuestion, firstAnswer

      if (questionAnswerPairs.length > 0) {
        const firstQuestionAnswerPair = questionAnswerPairs[0];
        
        firstQuestion = firstQuestionAnswerPair["question"];
        firstAnswer = firstQuestionAnswerPair["answer"];
        console.log(`First Key: ${firstQuestion}, First Value: ${firstAnswer}`);
      }
      
      navigate('/result', { state: { text: text, question: firstQuestion, answer: firstAnswer } });
    })
    .catch((error) => {
      console.log('API 요청 실패:', error);
      toast.error('글 전송에 실패했습니다.');
    });
  };

  const handleDeleteTextClick = () => {
    setText('');
  };

  return (
    <div className="App">
      <div className='box-description'>
        <p>분석하고 싶은 글을 입력해주세요</p>
      </div>

      <InputTextBox value={text} onChange={(e) => setText(e.target.value)} />

      <div className="mainpage-button-container">
        <NormalButton label="분석하기" onClick={ handleSendTextClick } />
        <NormalButton label="전체 삭제" onClick={ handleDeleteTextClick } />
        <Toaster
          position="top-right"
          reverseOrder={false}
        />
      </div>      
    </div>
  );
}

export default HomePage;
