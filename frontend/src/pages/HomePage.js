import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import toast, { Toaster } from "react-hot-toast";
import axios from "axios";

import NormalButton from "../components/NormalButton";
import InputTextBox from "../components/InputTextBox";
import "./HomePage.css";

function HomePage() {
  const [text, setText] = useState("");
  const navigate = useNavigate();
  const sample_answers = ["구조 개혁"];
  const API_URL =
    process.env.REACT_APP_API_URL || "http://localhost:8000/generate";
  const MIN_TEXT_LENGTH = 10;

  const handleSendTextClick = () => {
    if (text.length < MIN_TEXT_LENGTH) {
      toast.error("10자 이상 입력해주세요.");
      return;
    }
  
    axios
      .post(API_URL, {
        context: text,
        answers: sample_answers,
      })
      .then((response) => {
        const result_doc = response.data;
        const questionAnswerPairs = result_doc.question_answer_pairs;
        console.log("Question-Answer Pairs:", questionAnswerPairs);

        navigate("/result", {
          state: { text: text, questionAnswerPairs: questionAnswerPairs },
        });
      })
      .catch((error) => {
        console.log("API 요청 실패:", error);
        toast.error("글 전송에 실패했습니다.");
      });
  };

  const handleDeleteTextClick = () => {
    setText("");
  };

  return (
    <div>
      <header className="App-header">
        <h1>Reading Mate</h1>
      </header>

      <div className="mainpage-textbox-container">
        <InputTextBox 
          value={text} 
          onChange={(e) => setText(e.target.value)}
          />
      </div>
      <div className="mainpage-button-container">
        <NormalButton label="분석하기" onClick={handleSendTextClick} />
        <NormalButton label="전체 삭제" onClick={handleDeleteTextClick} />
      </div>

      <Toaster position="top-right" reverseOrder={false} />
    </div>
  );
}

export default HomePage;
