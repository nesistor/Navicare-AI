
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import ChatBox from "./Components/ChatBox";
import ImageUploader from "./Components/ImageUploader";
import "bootstrap/dist/css/bootstrap.min.css";
import logo  from "./assets/logo.jfif"

const Navbar = () => (
  <nav className="navbar navbar-expand-lg navbar-light bg-light">
    <div className="container">
      <Link className="navbar-brand" to="/">
        <img
          src={logo} 
          alt="Logo"
          className="rounded-circle"
          style={{ height: "40px", width: "40px" }}
        />
        <span className="ms-2">Hackathon App</span>
      </Link>
      <ul className="navbar-nav ms-auto">
        <li className="nav-item">
          <Link className="nav-link" to="/">
            Home
          </Link>
        </li>
        
      </ul>
    </div>
  </nav>
);


const Home = () => (
  <div className="d-flex justify-content-center align-items-center vh-100 bg-light">
    <div className="container bg-white p-4 rounded shadow" style={{ maxWidth: "600px" }}>
      <h2 className="text-center mb-4">AI ChatBot</h2>
      <ChatBox onSendMessage={(message) => console.log("ChatBot Message:", message)} />
      <div className="mt-4">
        <h4 className="text-center">Upload Image</h4>
        <ImageUploader onImageUpload={(image) => console.log("Uploaded Image:", image)} />
      </div>
    </div>
  </div>
);


const Prompt = () => (
  <div className="d-flex justify-content-center align-items-center vh-100 bg-light">
    <div className="container bg-white p-4 rounded shadow" style={{ maxWidth: "600px" }}>
      <h2 className="text-center">Prompt Page</h2>
      <ImageUploader onImageUpload={(image) => console.log("Uploaded Image:", image)} />
    </div>
  </div>
);


const App = () => (
  <Router>
    <Navbar />
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/prompt" element={<Prompt />} />
    </Routes>
  </Router>
);

export default App;
