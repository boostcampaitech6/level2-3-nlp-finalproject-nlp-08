import React, { useState } from "react";
import { useLocation } from "react-router-dom";
import FixedTextBox from "../components/FixedTextBox";
import NormalButton from "../components/NormalButton";
import QuestionBox from "../components/QuestionBox";
import CheckAnswerBox from "../components/CheckAnswerBox";
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
  const [userAnswer, setUserAnswer] = useState("");
  const [isAnswerCorrect, setIsAnswerCorrect] = useState(false);
  const [buttonClicked, setButtonClicked] = useState(false);

  const handleCheckAnswer = () => {
    setIsAnswerCorrect(userAnswer === correctAnswer);
    setButtonClicked(true);
  };

  return (
    <div>
      <header className="App-header">
        <h1>Reading Mate</h1>
      </header>
      <div className="mainpage-textbox-container">
        <FixedTextBox value={text} />
      </div>

      <div className="question-area">
        <QuestionBox value={question} />
      </div>
    </div>
  );
};

export default ResultPage;
