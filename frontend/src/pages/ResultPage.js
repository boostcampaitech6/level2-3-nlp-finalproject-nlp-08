import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useLocation } from "react-router-dom";
import FixedTextBox from "../components/FixedTextBox";
import QuestionBox from "../components/QuestionBox";
import { IoArrowUndoCircle } from "react-icons/io5";
import "./ResultPage.css";

const ResultPage = () => {
  const location = useLocation();
  console.log("Location state:", location.state);

  const text = location.state.text;
  const question = location.state.question;
  const correctAnswer = location.state.answer;
  console.log("Text:", text);
  console.log("Question:", question);
  console.log("Correct Answer:", correctAnswer);
  
  const navigate = useNavigate();

  const handleBackButtonClick = () => {
    navigate("/");
  };

  return (
    <div>
      <header className="App-header">
        <h1>Reading Mate</h1>
      </header>
      <div className="mainpage-textbox-container">
        <FixedTextBox value={text} answer={correctAnswer} />
        <IoArrowUndoCircle
          className="back-button"
          size="70"
          onClick={handleBackButtonClick}
        />
      </div>

      <div className="question-area">
        <QuestionBox value={question} />
      </div>
    </div>
  );
};

export default ResultPage;
