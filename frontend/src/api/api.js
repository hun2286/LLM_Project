// 백엔드 FastAPI와 통신 담당
// axios 사용해서 API 요청 -> JSON 응답 반환

import axios from "axios";

const API_URL = "http://localhost:8000"; 
// const API_URL = "https://ba3c785c25d1.ngrok-free.app"

export const askQuestion = async (question) => {
  try {
    const response = await axios.post(`${API_URL}/ask`, { question });
    return response.data.answer;
  } catch (error) {
    console.error("API 호출 오류:", error);
    return "답변을 가져오는 중 오류가 발생했습니다.";
  }
};

// export const askQuestion = async (question) => {
//   try {
//     const response = await axios.post(
//       `${API_URL}/ask`,
//       { question }, // save_pdf 없음
//       { headers: { "Content-Type": "application/json" } } // JSON 명시
//     );
//     return response.data.answer;
//   } catch (error) {
//     console.error("API 호출 오류:", error);
//     return "답변을 가져오는 중 오류가 발생했습니다.";
//   }
// };
