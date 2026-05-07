import { useState } from "react"
import { useNavigate } from "react-router-dom"

import api from "../services/api"

function Login() {

  const navigate = useNavigate()

  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  async function handleLogin(e) {
    e.preventDefault()

    try {

      const response = await api.post("/login", {
        email,
        password
      })

      // store token
      localStorage.setItem(
        "token",
        response.data.access_token
      )

      alert("Login success")

      navigate("/dashboard")

    } catch (err) {
      console.log(err)

      alert("Login failed")
    }
  }

  return (
    <div>

      <h1>Login</h1>

      <form onSubmit={handleLogin}>

        <input
          type="email"
          placeholder="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <br /><br />

        <input
          type="password"
          placeholder="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <br /><br />

        <button type="submit">
          Login
        </button>

      </form>

    </div>
  )
}

export default Login