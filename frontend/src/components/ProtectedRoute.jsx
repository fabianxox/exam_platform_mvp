//This component acts like:

//security guard

//No token:

//“go login”

//Token exists:

//“okay enter”
import { Navigate } from "react-router-dom"

function ProtectedRoute({ children }) {

  const token = localStorage.getItem("token")

  // no token → go login
  if (!token) {
    return <Navigate to="/" />
  }

  // token exists → allow page
  return children
}

export default ProtectedRoute   