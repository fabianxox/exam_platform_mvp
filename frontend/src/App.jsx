import { BrowserRouter, Routes, Route } from "react-router-dom"

import Login from "./pages/Login"
import Dashboard from "./pages/Dashboard"
import Exam from "./pages/Exam"
import Result from "./pages/Result"
import Signup from "./pages/signup"

import ProtectedRoute from "./components/ProtectedRoute"

function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route path="/" element={<Login />} />

        <Route path="/dashboard" element={
           <ProtectedRoute>
              <Dashboard />
           </ProtectedRoute>
        }/>

        <Route
  path="/exam/:id"
  element={
    <ProtectedRoute>
      <Exam />
    </ProtectedRoute>
  }
/>
       <Route path="/signup" element={<Signup />} />
        <Route
  path="/result/:id"
  element={
    <ProtectedRoute>
      <Result />
    </ProtectedRoute>
  }
/>

      </Routes>
    </BrowserRouter>
  )
}

export default App