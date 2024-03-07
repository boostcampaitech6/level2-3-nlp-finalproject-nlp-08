import React /*, { useState } */ from "react";
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

  const { questionAnswerPairs } = location.state;
  const questions = questionAnswerPairs.map((pair) => pair.question);
  const answers = questionAnswerPairs.map((pair) => pair.answer);
  const keywords = ["한국은행", "구조 개혁", "사회적 타협", "패스트 팔로어", "역동성"]
  console.log("Questions:", questions);
  console.log("Answers:", answers);

  const handleButtonClick = (clickedText, part) => {
    console.log(`Button clicked in ResultPage: ${clickedText}`);
    console.log(`Corresponding Part: ${part}`);
    // 여기에서 클릭 이벤트에 대한 추가 로직을 수행할 수 있습니다.
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
        <QuestionBox value={questions[0]} />
      </div>
    </div>
  );
};

export default ResultPage;
