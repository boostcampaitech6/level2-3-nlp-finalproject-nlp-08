import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { useLocation } from "react-router-dom";
import FixedTextBox from "../components/FixedTextBox";
import QuestionBox from "../components/QuestionBox";
import { IoArrowUndoCircle } from "react-icons/io5";
import { FaRegThumbsUp, FaRegThumbsDown } from "react-icons/fa";
import "./ResultPage.css";

const ResultPage = () => {
  const location = useLocation();
  console.log("Location state:", location.state);

  const text = location.state.text;
  console.log("Text:", text);

  const { questionAnswerPairs } = location.state;
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const questions = questionAnswerPairs.map((pair) => pair.question);
  const answers = questionAnswerPairs.map((pair) => pair.answer);
  const [isCorrect, setIsCorrect] = useState(null);
  const [isAllCorrect, setIsAllCorrect] = useState(false);
  const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000/feedback";
  console.log("Questions:", questions);
  console.log("Answers:", answers);
  const [submittedIssues, setSubmittedIssues] = useState(new Set());

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

  const handleFeedbackButtonClick = async (isLike) => {
    const currentQuestionAnswer = `${questions[currentQuestionIndex]}-${answers[currentQuestionIndex]}`;

    if (!submittedIssues.has(currentQuestionAnswer)) {
    try {
        const response = await axios.post(API_URL, {
          question: questions[currentQuestionIndex],
          answer: answers[currentQuestionIndex],
          context: text,
          like: isLike,
        });
        console.log('Feedback sent successfully:', response.data);
        setSubmittedIssues(new Set([...submittedIssues, currentQuestionAnswer]));
      } catch (error) {
        console.error('Error sending feedback:', error);
      }
    } else {
      console.log('Issue already submitted as feedback');
    };
  };

  return (
    <div>
      <header className="App-header">
        <h1>Reading Mate</h1>
      </header>
      <div className="mainpage-textbox-container">
        <FixedTextBox value={text} keywords={answers} onButtonClick={handleButtonClick}/>
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

      <div className="like-dislike-area">
        <FaRegThumbsUp className="likeFeedbackButton" onClick={() => handleFeedbackButtonClick(true)} />
        <FaRegThumbsDown className="disLikeFeedbackButton" onClick={() => handleFeedbackButtonClick(false)} />
      </div>
    </div>
  );
};

export default ResultPage;
