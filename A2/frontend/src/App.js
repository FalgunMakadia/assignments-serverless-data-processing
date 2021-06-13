import { BrowserRouter, Route } from 'react-router-dom'
import './App.css'
import Register from './components/Register'
import Login from './components/Login'
import Dashboard from './components/Dashboard'
import Home from './components/Home'

function App() {
  return (
    <BrowserRouter>
      <main>
        <Route path='/register' component={Register} />
        <Route path='/login' component={Login} />
        <Route path='/dashboard' component={Dashboard} />
        <Route path='/' component={Home} exact />
      </main>
    </BrowserRouter>
  )
}

export default App
