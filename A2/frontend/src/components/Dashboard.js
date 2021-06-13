import axios from 'axios'
import React, { useEffect, useState } from 'react'
import { useHistory } from 'react-router-dom'

const Dashboard = ({ location }) => {
  const history = useHistory()
  const email = location.search.split('=')[1]

  const [activeUserList, setActiveUserList] = useState({})

  const getActiveUsers = async () => {
    try {
      const { status, message, active_users } = await axios.get(
        'https://c3-6465pw2r5q-ue.a.run.app/dashboard'
      )
      alert(message)
      if (status === 'true') {
        setActiveUserList(active_users)
      }
    } catch (e) {
      alert(e)
    }
  }

  useEffect(() => {
    getActiveUsers()
  })

  const logout = async () => {
    try {
      const { message } = await axios.get(
        'https://c3-6465pw2r5q-ue.a.run.app/logout',
        { email }
      )
      alert(message)
      history.push('/login')
    } catch (e) {
      alert(e)
    }
  }

  return (
    <div
      style={{
        border: '1px black solid',
        margin: '25px 50px',
        marginTop: '100px',
        fontFamily: 'sans-serif',
      }}
    >
      <h3 style={{ textAlign: 'center' }}>Welcome falgun@gmail.com</h3>
      <hr />
      <div style={{ marginLeft: '30px' }}>
        <h2>Online Users:</h2>
        <ul>
          <li>chandler@gmail.com</li>
          <li>sherlock@gmail.com</li>
        </ul>
      </div>
      <hr />
      <div style={{ textAlign: 'center', marginBottom: '10px' }}>
        <button onClick={logout} style={{ padding: '5px', fontSize: 'medium' }}>
          Logout
        </button>
      </div>
    </div>
  )
}

export default Dashboard

// {activeUserList &&
//   activeUserList.map((user, index) => {
//     return (
//       <ul key={index}>
//         <li>{user[0]}</li>
//       </ul>
//     )
//   })}

// <h3 style={{ textAlign: 'center' }}>Welcome {email}</h3>
