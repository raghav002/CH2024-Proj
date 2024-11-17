import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min'; // Import Bootstrap's JS bundle for modal functionality
import React, { useState } from 'react';
import './App.css';

const App = () => {
  const [formData, setFormData] = useState({ major: '', goals: '' });
  const [generatedPlan, setGeneratedPlan] = useState('');
  const [selectedCard, setSelectedCard] = useState(null); // State for the clicked card

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // HARDCODED FOR NOW - will be replaced by AI model
    const plan = [
      { title: "Semester 1: Fall Year 1", courses: ["Course 1: [Name] - [Credits]", "Course 2: [Name] - [Credits]", "Course 3: [Name] - [Credits]", "Course 4: [Name] - [Credits]"], totalCredits: "[Total]" },
      { title: "Semester 2: Spring Year 1", courses: ["Course 1: [Name] - [Credits]", "Course 2: [Name] - [Credits]", "Course 3: [Name] - [Credits]", "Course 4: [Name] - [Credits]"], totalCredits: "[Total]" },
      { title: "Semester 3: Summer Year 1", courses: ["Course 1: [Name] - [Credits]", "Course 2: [Name] - [Credits]", "Course 3: [Name] - [Credits]", "Course 4: [Name] - [Credits]"], totalCredits: "[Total]" },
      { title: "Semester 4: Fall Year 2", courses: ["Course 1: [Name] - [Credits]", "Course 2: [Name] - [Credits]", "Course 3: [Name] - [Credits]", "Course 4: [Name] - [Credits]"], totalCredits: "[Total]" },
      { title: "Semester 5: Spring Year 2", courses: ["Course 1: [Name] - [Credits]", "Course 2: [Name] - [Credits]", "Course 3: [Name] - [Credits]", "Course 4: [Name] - [Credits]"], totalCredits: "[Total]" },
      { title: "Semester 6: Summer Year 2", courses: ["Course 1: [Name] - [Credits]", "Course 2: [Name] - [Credits]", "Course 3: [Name] - [Credits]", "Course 4: [Name] - [Credits]"], totalCredits: "[Total]" },
      { title: "Semester 7: Fall Year 3", courses: ["Course 1: [Name] - [Credits]", "Course 2: [Name] - [Credits]", "Course 3: [Name] - [Credits]", "Course 4: [Name] - [Credits]"], totalCredits: "[Total]" },
      { title: "Semester 8: Spring Year 3", courses: ["Course 1: [Name] - [Credits]", "Course 2: [Name] - [Credits]", "Course 3: [Name] - [Credits]", "Course 4: [Name] - [Credits]"], totalCredits: "[Total]" },
      { title: "Semester 9: Summer Year 3", courses: ["Course 1: [Name] - [Credits]", "Course 2: [Name] - [Credits]", "Course 3: [Name] - [Credits]", "Course 4: [Name] - [Credits]"], totalCredits: "[Total]" },
      { title: "Semester 10: Fall Year 4", courses: ["Course 1: [Name] - [Credits]", "Course 2: [Name] - [Credits]", "Course 3: [Name] - [Credits]", "Course 4: [Name] - [Credits]"], totalCredits: "[Total]" },
      { title: "Semester 11: Spring Year 4", courses: ["Course 1: [Name] - [Credits]", "Course 2: [Name] - [Credits]", "Course 3: [Name] - [Credits]", "Course 4: [Name] - [Credits]"], totalCredits: "[Total]" },
      { title: "Semester 12: Summer Year 4", courses: ["Course 1: [Name] - [Credits]", "Course 2: [Name] - [Credits]", "Course 3: [Name] - [Credits]", "Course 4: [Name] - [Credits]"], totalCredits: "[Total]" }
    ];
    
    setGeneratedPlan(plan);
  };

  return (
    <div className="App">
      {/* Navbar */}
      <header className="bg-primary text-white py-3">
        <nav className="navbar navbar-expand-lg navbar-dark bg-primary container">
          <a className="navbar-brand" href="/">Your 4-Year Plan</a>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
            aria-controls="navbarNav"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav ms-auto">
              <li className="nav-item">
                <a href="#about" className="nav-link text-white">About</a>
              </li>
              <li className="nav-item">
                <a href="#generate" className="nav-link text-white">Generate Plan</a>
              </li>
              <li className="nav-item">
                <a href="#contact" className="nav-link text-white">Contact</a>
              </li>
            </ul>
          </div>
        </nav>
      </header>

      {/* Hero Section */}
      <section id="hero" className="bg-dark text-white text-center py-5">
        <div className="container">
          <h1 className="display-4">Welcome to Your Personalized 4-Year Plan Powered by AI</h1>
          <p className="lead">Let AI help you map out your next four years for academic and professional success!</p>
          <a href="#generate" className="btn btn-warning btn-lg">Get Started</a>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-5">
        <div className="container">
          <h2 className="text-center mb-4">How It Works</h2>
          <p className="text-center">Our AI-powered tool analyzes your goals and interests to create a tailored 4-year plan to guide you through college, career growth, and personal development.</p>
        </div>
      </section>

      {/* Generate Plan Section */}
      <section id="generate" className="py-5 bg-light">
        <div className="container">
          <h2 className="text-center mb-4">Generate Your Plan</h2>
          <form onSubmit={handleSubmit} className="mb-4">
            <div className="mb-3">
              <label htmlFor="interests" className="form-label">What are your interests?</label>
              <input
                type="text"
                id="interests"
                name="interests"
                className="form-control"
                placeholder="ex. Web Development"
                value={formData.major}
                onChange={handleChange}
                required
              />
            </div>
            <div className="mb-3">
              <label htmlFor="credits" className="form-label">How many credits per semester?</label>
              <textarea
                id="credits"
                name="credits"
                className="form-control"
                placeholder="ex. 15"
                value={formData.goals}
                onChange={handleChange}
                required
              ></textarea>
            </div>
            <div className="mb-3">
              <label htmlFor="transfer_credits" className="form-label">How many transfer credits do you have?</label>
              <textarea
                id="transfer_credits"
                name="transfer_credits"
                className="form-control"
                placeholder="ex. 4"
                value={formData.goals}
                onChange={handleChange}
                required
              ></textarea>
            </div>
            <div className="mb-3">
              <label htmlFor="completed_courses" className="form-label">Which classes have you completed?</label>
              <textarea
                id="completed_courses"
                name="completed_courses"
                className="form-control"
                placeholder="ex. CS200, MATH222"
                value={formData.goals}
                onChange={handleChange}
                required
              ></textarea>
            </div>
            <button type="submit" className="btn btn-primary w-100">Generate Plan</button>
          </form>

          {/* Render Generated Plan */}
          {generatedPlan && (
            <div className="plan-container d-flex flex-wrap gap-3">
              {generatedPlan.map((card, index) => (
                <div
                  key={index}
                  className="card shadow-sm"
                  style={{ width: '18rem', cursor: 'pointer' }}
                  onClick={() => setSelectedCard(card)} // Set the clicked card
                >
                  <div className="card-body">
                    <h5 className="card-title">{card.title}</h5>
                    <ul>
                      {card.courses.map((course, i) => (
                        <li key={i}>{course}</li>
                      ))}
                    </ul>
                    <p><strong>Total Credits:</strong> {card.totalCredits}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Modal for Selected Card */}
      {selectedCard && (
        <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">{selectedCard.title}</h5>
                <button type="button" className="btn-close" onClick={() => setSelectedCard(null)}></button>
              </div>
              <div className="modal-body">
                <ul>
                  {selectedCard.courses.map((course, i) => (
                    <li key={i}>{course}</li>
                  ))}
                </ul>
                <p><strong>Total Credits:</strong> {selectedCard.totalCredits}</p>
              </div>
              <div className="modal-footer">
                <button className="btn btn-secondary" onClick={() => setSelectedCard(null)}>Close</button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="bg-primary text-white text-center py-3">
        <p>&copy; 2024 Your 4-Year Plan. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default App;
