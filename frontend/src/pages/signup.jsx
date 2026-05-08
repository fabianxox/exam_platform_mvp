import { useState } from "react"
import { useNavigate } from "react-router-dom"

import api from "../services/api"

function Signup() {

  const [email, setEmail] = useState("")

  const [password, setPassword] = useState("")

  const navigate = useNavigate()

  async function handleSignup(e) {

    e.preventDefault()

    try {

      await api.post("/user", {
        email,
        password
      })

      alert("Account created successfully")

      navigate("/")

    } catch (err) {

      console.log(err)

      alert("Signup failed")
    }
  }

  return (

    <div className="min-h-screen flex items-center justify-center bg-gray-100">

      <form
        onSubmit={handleSignup}
        className="bg-white p-8 rounded-xl shadow-md w-80"
      >

        <h1 className="text-2xl font-bold mb-6 text-center">
          Signup
        </h1>

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full border p-2 rounded mb-4"
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full border p-2 rounded mb-4"
        />

        <button
          type="submit"
          className="w-full bg-green-500 text-white p-2 rounded"
        >
          Create Account
        </button>

      </form>

    </div>
  )
}

export default Signup