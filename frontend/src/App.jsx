import { BrowserRouter, Routes, Route } from "react-router-dom"

import Login from "./pages/Login"
import Dashboard from "./pages/Dashboard"
import Exam from "./pages/Exam"
import Result from "./pages/Result"

function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route path="/" element={<Login />} />

        <Route path="/dashboard" element={<Dashboard />} />

        <Route path="/exam/:id" element={<Exam />} />

        <Route path="/result/:id" element={<Result />} />

      </Routes>
    </BrowserRouter>
  )
}

export default App