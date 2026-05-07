import { useEffect, useState } from "react"
import { useNavigate, useParams } from "react-router-dom"

import api from "../services/api"

function Exam() {

  const { id } = useParams()

  const navigate = useNavigate()

  const [exam, setExam] = useState(null)

  const [answers, setAnswers] = useState([])

  useEffect(() => {

    async function loadExam() {

      try {

        const token = localStorage.getItem("token")

        // start attempt
        await api.post(
          `/exam/${id}/start`,
          {},
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )

        // fetch exam
        const response = await api.get(
          `/exam/${id}`,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )

        setExam(response.data)

      } catch (err) {
        console.log(err)
      }
    }

    loadExam()

  }, [])

  function selectAnswer(questionId, answer) {

    setAnswers((prev) => {

      // remove old answer if exists
      const filtered = prev.filter(
        (a) => a.question_id !== questionId
      )

      return [
        ...filtered,
        {
          question_id: questionId,
          answer: answer
        }
      ]
    })
  }

  async function submitExam() {

    try {

      const token = localStorage.getItem("token")

      await api.post(
        `/exam/${id}/submit`,
        {
          answers: answers
        },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      navigate(`/result/${id}`)

    } catch (err) {
      console.log(err)
    }
  }

  if (!exam) {
    return <h1>Loading...</h1>
  }

  return (
    <div>

      <h1>{exam.title}</h1>

      <p>Duration: {exam.duration} mins</p>

      <hr />

      {exam.questions.map((q) => (

        <div key={q.id}>

          <h3>{q.text}</h3>

          <button
            onClick={() => selectAnswer(q.id, q.option_a)}
          >
            {q.option_a}
          </button>

          <br /><br />

          <button
            onClick={() => selectAnswer(q.id, q.option_b)}
          >
            {q.option_b}
          </button>

          <br /><br />

          <button
            onClick={() => selectAnswer(q.id, q.option_c)}
          >
            {q.option_c}
          </button>

          <br /><br />

          <button
            onClick={() => selectAnswer(q.id, q.option_d)}
          >
            {q.option_d}
          </button>

          <hr />

        </div>

      ))}

      <button onClick={submitExam}>
        Submit Exam
      </button>

    </div>
  )
}

export default Exam