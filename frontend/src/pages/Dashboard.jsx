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

        // pagination response
        setExams(response.data.items)

      } catch (err) {

        console.log(err)
      }
    }

    fetchExams()

  }, [])

  function logout() {

    localStorage.removeItem("token")

    navigate("/")
  }

  return (

    <div className="min-h-screen bg-gray-100 p-6">

      <div className="flex justify-between items-center mb-6">

        <h1 className="text-3xl font-bold">
          Dashboard
        </h1>

        <button
          onClick={logout}
          className="bg-red-500 text-white px-4 py-2 rounded"
        >
          Logout
        </button>

      </div>

      {exams.length === 0 ? (

        <p>No exams available</p>

      ) : (

        exams.map((exam) => (

          <div
            key={exam.id}
            className="bg-white p-4 rounded-xl shadow mb-4"
          >

            <h2 className="text-xl font-bold">
              {exam.title}
            </h2>

            <p className="text-gray-600">
              Duration: {exam.duration} mins
            </p>

            <button
              onClick={() => navigate(`/exam/${exam.id}`)}
              className="mt-4 bg-green-500 text-white px-4 py-2 rounded"
            >
              Start Exam
            </button>

          </div>

        ))

      )}

    </div>
  )
}

export default Dashboard