// import logo from './logo.svg';
import './App.css';
import './output.css'
import Navbar from './components/Navbar';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/Home';
import Train from './components/Train';
import './output.css'
import './spinner.css'
import './popup.css'
import Footer from './components/Footer';
import Gen from './components/Gen';
import Login from './components/Login';
function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/train" element={<Train />} />
        <Route path="/gen" element={<Gen />} />
        <Route path="/login" element={<Login />} />
      </Routes>
      <Footer />
    </Router>

  );
}

export default App;
