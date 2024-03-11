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
  console.log("Text:", text);

  const dummyquestions = ["한국은행이 답인 문제", "구조 개혁이 답인 문제", "사회적 타협이 답인 문제"];
  const dummyanswers = ["한국은행", "구조 개혁", "사회적 타협"];

  // const { questionAnswerPairs } = location.state;
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  // const questions = questionAnswerPairs.map((pair) => pair.question);
  // const answers = questionAnswerPairs.map((pair) => pair.answer);
  const [isCorrect, setIsCorrect] = useState(null);
  const [isAllCorrect, setIsAllCorrect] = useState(false);
  const questions = dummyquestions;
  const answers = dummyanswers;
  const keywords = ["한국은행", "구조 개혁", "사회적 타협", "패스트 팔로어", "골든 타임"]
  console.log("Questions:", questions);
  console.log("Answers:", answers);

  const handleButtonClick = (clickedText) => {
    console.log(`Button clicked in ResultPage: ${clickedText}`);
    if (clickedText === answers[currentQuestionIndex]) {
      console.log("Correct!");
      setIsCorrect(true);
      setTimeout(() => {
        if (currentQuestionIndex < questions.length - 1) {
          setCurrentQuestionIndex(currentQuestionIndex + 1);
          setIsCorrect(null);
        } else {
          console.log("All questions answered!");
          setIsAllCorrect(true);
        }
      }, 1600);
    } else {
      console.log("Incorrect!");
      setIsCorrect(false);
      setTimeout(() => {
        setIsCorrect(null);
      }, 1000);
    }
  };

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
        <FixedTextBox value={text} keywords={keywords} onButtonClick={handleButtonClick}/>
        <IoArrowUndoCircle
          className="back-button"
          size="70"
          onClick={handleBackButtonClick}
        />
      </div>

      <div className="question-area">
        <QuestionBox 
          value={questions[currentQuestionIndex]} 
          isCorrect={isCorrect} 
          isAllCorrect={isAllCorrect}
        />
      </div>
    </div>
  );
};

export default ResultPage;
