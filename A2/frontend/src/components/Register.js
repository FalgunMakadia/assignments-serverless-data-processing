import React, { useState } from 'react'
import axios from 'axios'
import Dropdown from 'react-dropdown'
import { useHistory } from 'react-router-dom'

const Register = () => {
  const history = useHistory()

  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [topic, setTopic] = useState('')

  const topics = [
    'Food',
    'Valorant',
    'CSGO',
    'Sports',
    'Game Of Thrones',
    'Netflix',
    'FRIENDS',
  ]

  const validateAndRegister = async () => {
    const regEx = /^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[A-Za-z]+$/
    const validEmail = regEx.test(email)

    if (!name || name.trim() === '') {
      alert('Name can not be empty!')
      return
    }
    if (!email || email.trim() === '') {
      alert('Email can not be empty!')
      return
    }
    if (!validEmail) {
      alert('Invalid Email!')
      return
    }
    if (!password || password.trim() === '') {
      alert('Password can not be empty!')
      return
    }
    if (password.length < 6) {
      alert('Password should be 6 characters or long!')
      return
    }

    try {
      const { msg } = await axios.post(
        'https://c1-6465pw2r5q-ue.a.run.app/register',
        {
          name,
          email,
          password,
          topic,
        }
      )
      alert(msg)
      history.push('/dashboard?email=' + email)
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
      <h2>Registration</h2>
      <hr />
      <br />
      <div>
        <strong>Name: </strong>
        <input
          type='text'
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
      </div>
      <div>
        <strong>Email: </strong>
        <input value={email} onChange={(e) => setEmail(e.target.value)} />
      </div>
      <div>
        <strong>Password: </strong>
        <input
          type='password'
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>
      <div>
        <strong>Topic: </strong>
        <div
          style={{
            border: '1px solid black',
            margin: '0px 300px',
            cursor: 'pointer',
          }}
        >
          <Dropdown
            options={topics}
            onChange={(value) => setTopic(value)}
            value={topic}
          />
        </div>
      </div>
      <br />
      <div>
        <button
          onClick={validateAndRegister}
          style={{ padding: '5px', fontSize: 'medium' }}
        >
          Register
        </button>
        <br />
        <br />
        Click <a href='/login'>here</a> to Login
        <br />
        <br />
      </div>
    </div>
  )
}
export default Register
