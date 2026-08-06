import { API } from './api/api';
import './index.css';
import { useState } from 'react';
import { useNavigate } from "react-router-dom";

export function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    try {

      const response = await API.post("/login", formData, {headers: {"Content-Type":"application/x-www-form-urlencoded"}});
      console.log(response.data);
      
      localStorage.setItem(
        "access_token", 
        response.data.access_token);
        alert("Login successful");

        navigate("/profile")

    }catch(error) {

      console.log(error);

      alert(
        error.response?.data?.detail || 
        "Login failed"
      );
    }
  }

  return (
    <>
      <div>
        <form className='container' onSubmit={handleLogin}>
          <h1>Login</h1>
          <input type="text" placeholder='Username' className='form f1' value={username} onChange={(e)=>setUsername(e.target.value)}/>
          <input type="password" placeholder='Password' className='form f3' value={password} onChange={(e)=>setPassword(e.target.value)}/>
          {/* <input type="email" placeholder='Email' className='form f2'/> */}
          <button className='submitBtn'>Submit</button>
        </form>
      </div>
    </>
  )
}
