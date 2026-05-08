import { useEffect, useState } from "react"
import { useNavigate, useParams } from "react-router-dom"

import api from "../services/api"

function Exam() {

  const { id } = useParams()

  const navigate = useNavigate()

  const [exam, setExam] = useState(null)

  const [answers, setAnswers] = useState([])

  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {

    async function loadExam() {

      try {

        const token = localStorage.getItem("token")

        // start or reuse attempt
        await api.post(
          `/exam/${id}/start`,
          {},
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )

        // fetch exam data
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

        console.log(err.response?.data)
      }
    }

    loadExam()

  }, [])

  // select answer
  function selectAnswer(questionId, answer) {

    setAnswers((prev) => {

      // remove previous answer
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

  // check selected option
  function isSelected(questionId, option) {

    return answers.some(
      (a) =>
        a.question_id === questionId &&
        a.answer === option
    )
  }

  // submit exam
  async function submitExam() {

    try {

      setSubmitting(true)

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

      console.log(err.response?.data)

      setSubmitting(false)
    }
  }

  // loading state
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

          {/* OPTION A */}
          <button
            onClick={() => selectAnswer(q.id, q.option_a)}

            style={{
              backgroundColor: isSelected(
                q.id,
                q.option_a
              )
                ? "green"
                : "white",

              color: isSelected(
                q.id,
                q.option_a
              )
                ? "white"
                : "black"
            }}
          >
            {q.option_a}
          </button>

          <br /><br />

          {/* OPTION B */}
          <button
            onClick={() => selectAnswer(q.id, q.option_b)}

            style={{
              backgroundColor: isSelected(
                q.id,
                q.option_b
              )
                ? "green"
                : "white",

              color: isSelected(
                q.id,
                q.option_b
              )
                ? "white"
                : "black"
            }}
          >
            {q.option_b}
          </button>

          <br /><br />

          {/* OPTION C */}
          <button
            onClick={() => selectAnswer(q.id, q.option_c)}

            style={{
              backgroundColor: isSelected(
                q.id,
                q.option_c
              )
                ? "green"
                : "white",

              color: isSelected(
                q.id,
                q.option_c
              )
                ? "white"
                : "black"
            }}
          >
            {q.option_c}
          </button>

          <br /><br />

          {/* OPTION D */}
          <button
            onClick={() => selectAnswer(q.id, q.option_d)}

            style={{
              backgroundColor: isSelected(
                q.id,
                q.option_d
              )
                ? "green"
                : "white",

              color: isSelected(
                q.id,
                q.option_d
              )
                ? "white"
                : "black"
            }}
          >
            {q.option_d}
          </button>

          <hr />

        </div>

      ))}

      <button
        onClick={submitExam}

        disabled={submitting}
      >

        {
          submitting
            ? "Submitting..."
            : "Submit Exam"
        }

      </button>

    </div>
  )
}

export default Exam