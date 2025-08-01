import { HashRouter as Router, Routes, Route} from 'react-router-dom'

import { User } from './Pages/User'
import { LearnList } from './Pages/LearnList'


function App() {
  

  
  return (
    <Router>
      <Routes>
          <Route path='/' element={<User />} />
          <Route path='/LearnList' element={<LearnList />}/>
      </Routes>
    </Router>
  )
}

export default App
