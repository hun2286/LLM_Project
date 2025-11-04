// questioninput과 answerdisplay 조합하고 상태 관리 담당
// 질문을 입력하고 버튼 클릭시 API 호출 -> 답변 받아와서 화면에서 보여주는 역할

import React, { useState } from "react";
import QuestionInput from "./components/QuestionInput";
import AnswerDisplay from "./components/AnswerDisplay";
import { askQuestion } from "./api/api";
import "./App.css";

export default function App() {
  const [answer, setAnswer] = useState("");

  const handleQuestion = async (question) => {
    const response = await askQuestion(question);
    setAnswer(response);
  };

  return (
    <div className="app-container">
      <div className="input-section">
        <QuestionInput onSubmit={handleQuestion} />
      </div>
      {answer && (
        <div className="answer-section">
          <AnswerDisplay answer={answer} />
        </div>
      )}
    </div>
  );
}
