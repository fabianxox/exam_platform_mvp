import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"

import api from "../services/api"

function Dashboard() {

  const [exams, setExams] = useState([])

  const navigate = useNavigate()

  useEffect(() => {

    async function fetchExams() {

      try {

        const token = localStorage.getItem("token")

        const response = await api.get("/exams", {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })

        setExams(response.data)

      } catch (err) {
        console.log(err)
      }
    }

    fetchExams()

  }, [])

  return (
    <div>

      <h1>Dashboard</h1>

      {exams.map((exam) => (

        <div key={exam.id}>

          <h3>{exam.title}</h3>

          <p>Duration: {exam.duration} mins</p>

          <button
            onClick={() => navigate(`/exam/${exam.id}`)}
          >
            Start Exam
          </button>

          <hr />

        </div>

      ))}

    </div>
  )
}

export default Dashboard