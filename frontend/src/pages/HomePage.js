import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import toast, { Toaster } from "react-hot-toast";
import axios from "axios";

import NormalButton from "../components/NormalButton";
import InputTextBox from "../components/InputTextBox";
import placeholder  from "../components/PlaceHolder";
import LoadingPage from './LoadingPage';
import "./HomePage.css";

function HomePage() {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const API_URL =
    process.env.REACT_APP_API_URL || "http://localhost:8000/generate";
  const MIN_TEXT_LENGTH = 10;

  const default_text = placeholder.split("예시)\n")[1]

  const handleSendTextClick = () => {
    let inputText = text
    if (inputText.length === 0) {
      inputText = default_text
    }
    else if (inputText.length < MIN_TEXT_LENGTH) {
      toast.error("10자 이상 입력해주세요.");
      return;
    }

    setLoading(true)
    axios.post(API_URL, { 
      context: inputText,
      answers: [],
      num_to_generate: 5
    })
    .then((response) => {
      const result_doc  = response.data;
      const questionAnswerPairs = result_doc.question_answer_pairs;
      console.log("Question-Answer Pairs:", questionAnswerPairs);

      navigate("/result", {
        state: { text: inputText, questionAnswerPairs },
      });
    })
    .catch((error) => {
      console.log('API 요청 실패:', error);
      toast.error('글 전송에 실패했습니다.');
    })
    .finally(() => {
      setLoading(false);
    });
  };

  const handleDeleteTextClick = () => {
    setText("");
  };

  return (
    <div>
      {loading ? (<LoadingPage />) : (
      <div>
        <header className="App-header">
          <h1>Reading Mate</h1>
        </header>

        <div className="mainpage-textbox-container">
          <InputTextBox 
            value={text} 
            onChange={(e) => setText(e.target.value)}
            placeholder={placeholder}
          />
        </div>

        <div className="mainpage-button-container">
          <NormalButton label="분석하기" onClick={ handleSendTextClick } />
          <NormalButton label="전체 삭제" onClick={ handleDeleteTextClick } />
          <Toaster
            position="top-right"
            reverseOrder={false}
          />
        </div>
      </div>
      )}
    </div>
  );
}

export default HomePage;
