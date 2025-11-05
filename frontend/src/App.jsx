// questioninput과 answerdisplay 조합하고 상태 관리 담당
// 질문을 입력하고 버튼 클릭시 API 호출 -> 답변 받아와서 화면에서 보여주는 역할

// App.jsx
import React, { useState } from "react";
import QuestionInput from "./components/QuestionInput";
import AnswerDisplay from "./components/AnswerDisplay";
import "./App.css";

function App() {
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [lastQuestion, setLastQuestion] = useState("");

  // 질문 전송 로직
  const handleAsk = async (question) => {
    if (!question.trim()) return alert("질문을 입력하세요!");
    setLoading(true);
    setAnswer("");
    setLastQuestion(question);

    try {
      const response = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      const data = await response.json();
      setAnswer(data.answer);
    } catch (error) {
      console.error(error);
      alert("서버 요청 중 오류가 발생했습니다.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <h1 className="app-title">PDF QA 시스템</h1>

      {/* 질문 입력 */}
      <div className="question-wrapper">
        <QuestionInput onSubmit={handleAsk} />
      </div>

      {/* 답변 로딩 표시 */}
      {loading && <p className="loading-text">답변 생성 중...</p>}

      {/* 답변 표시 */}
      {answer && (
        <div className="answer-wrapper">
          {/* 질문 표시 */}
          <p className="question-display">
          질문 : {lastQuestion}
          </p>

          {/* 실제 답변 */}
          <AnswerDisplay answer={answer} />
        </div>
      )}
    </div>
  );
}

export default App;

