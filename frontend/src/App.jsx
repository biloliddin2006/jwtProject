import { Routes, Route } from "react-router-dom";
import { Profile } from "./pages/Profile";
import { Login } from "./Login";

export function App(){
  return(
    <Routes>

      <Route path="/" element={<Login />}></Route>
      <Route path="/profile" element={<Profile />}></Route>

    </Routes>
  )
}