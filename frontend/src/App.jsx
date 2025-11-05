// questioninput과 answerdisplay 조합하고 상태 관리 담당
// 질문을 입력하고 버튼 클릭시 API 호출 -> 답변 받아와서 화면에서 보여주는 역할

import React, { useState } from "react";
import QuestionInput from "./components/QuestionInput";
import AnswerDisplay from "./components/AnswerDisplay";
import { askQuestion } from "./api/api";
import "./App.css";

export default function App() {
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false); // ✅ 로딩 상태 추가
  const [error, setError] = useState(""); // (선택) 에러 처리

  const handleQuestion = async (question) => {
    setLoading(true);     // ✅ 로딩 시작
    setAnswer("");
    setError("");

    try {
      const response = await askQuestion(question);
      setAnswer(response);
    } catch (err) {
      setError("⚠️ 답변을 불러오는 중 오류가 발생했습니다.");
    } finally {
      setLoading(false);  // ✅ 로딩 종료
    }
  };

  return (
    <div className="app-container">
      <div className="input-section">
        <QuestionInput onSubmit={handleQuestion} />
      </div>

      {loading && ( // ✅ 로딩 상태 표시
        <div className="loading-section">
          <p style={{ color: "#666" }}>🕐 답변을 생성 중입니다...</p>
        </div>
      )}

      {error && ( // (선택) 에러 표시
        <div className="error-section">
          <p style={{ color: "red" }}>{error}</p>
        </div>
      )}

      {answer && !loading && ( // ✅ 로딩이 끝난 뒤에만 답변 표시
        <div className="answer-section">
          <AnswerDisplay answer={answer} />
        </div>
      )}
    </div>
  );
}
