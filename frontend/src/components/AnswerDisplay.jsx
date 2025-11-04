// 백엔드에서 받은 답변 표시 UI

export default function AnswerDisplay({ answer }) {

  const formattedAnswer = answer.replace(/\s*(\[출처:.*?\])/g, '\n$1');

  return (
    <div style={{ whiteSpace: 'pre-line', textAlign: 'center', margin: '20px' }}>
      <h2>답변</h2>
      <p>{formattedAnswer}</p>
    </div>
  );
}
