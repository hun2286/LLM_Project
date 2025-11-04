// 질문 입력 UI 컴포넌트
// 입력값을 App으로 전달하는 이벤트 처리 담당

import React, { useState } from "react";

export default function QuestionInput({ onSubmit }) {
  const [question, setQuestion] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (question.trim() !== "") {
      onSubmit(question);
      setQuestion("");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="질문을 입력하세요"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />
      <button type="submit">확인</button>
    </form>
  );
}
