import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"

import api from "../services/api"

function Result() {

  const { id } = useParams()

  const [result, setResult] = useState(null)

  useEffect(() => {

    async function fetchResult() {

      try {

        const token = localStorage.getItem("token")

        const response = await api.get(
          `/exam/${id}/result`,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )

        setResult(response.data)

      } catch (err) {
        console.log(err)
      }
    }

    fetchResult()

  }, [])

  if (!result) {
    return <h1>Loading...</h1>
  }

  return (
    <div>

      <h1>Exam Result</h1>

      <h2>Score: {result.score}</h2>

    </div>
  )
}

export default Result