import React, { useState } from 'react'
import { useHistory } from 'react-router-dom'
import axios from 'axios'

const Login = () => {
  const history = useHistory()

  const [email, setEmail] = useState()
  const [password, setPassword] = useState()

  const login = async () => {
    if (!email || email.trim() === '') {
      alert('Email can not be empty!')
      return
    }
    if (!password || password.trim() === '') {
      alert('Password can not be empty!')
      return
    }
    try {
      const { status, msg } = await axios.get(
        'https://c2-6465pw2r5q-ue.a.run.app/login',
        { email, password }
      )
      if (status === 'true') {
        alert(msg)
        history.push('/dashboard?email=' + email)
      } else {
        alert(msg)
      }
    } catch (e) {
      alert(e)
    }
  }

  return (
    <div
      style={{
        textAlign: 'center',
        border: '1px black solid',
        margin: '25px 50px',
        marginTop: '100px',
        fontFamily: 'sans-serif',
      }}
    >
      <h2>Login</h2>
      <hr />
      <br />
      <div>
        <strong>Email: </strong>
        <input
          type='text'
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>

      <div>
        <strong>Password: </strong>
        <input
          type='password'
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>
      <br />
      <div>
        <button onClick={login} style={{ padding: '5px', fontSize: 'medium' }}>
          Login
        </button>
        <br />
        <br />
        Click <a href='/register'>here</a> to Register
        <br />
        <br />
      </div>
    </div>
  )
}

export default Login
