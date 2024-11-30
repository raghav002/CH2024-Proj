import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min';
import React, { useState } from 'react';
import './App.css';

const App = () => {
  const [formData, setFormData] = useState({
    interests: '',
    credits: '',
    transferCredits: '',
    completedCourses: '',
  });
  const [generatedPlan, setGeneratedPlan] = useState([]);
  const [selectedCard, setSelectedCard] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Mock Data for Generated Plan
    const plan = [
      {
        title: 'Semester 1: Fall Year 1',
        courses: ['Intro to Programming', 'Math 101', 'English 101', 'History 101'],
        totalCredits: '15',
      },
      {
        title: 'Semester 2: Spring Year 1',
        courses: ['Data Structures', 'Physics 101', 'Art 101', 'Philosophy 101'],
        totalCredits: '16',
      },
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
            </ul>
          </div>
        </nav>
      </header>

      {/* Hero Section */}
      <section id="hero" className="bg-dark text-white text-center py-5">
        <div className="container">
          <h1 className="display-4">Welcome to Your Personalized 4-Year Plan</h1>
          <p className="lead">Let AI help you map out your next four years for academic and professional success!</p>
          <a href="#generate" className="btn btn-warning btn-lg">Get Started</a>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-5">
        <div className="container">
          <h2 className="text-center mb-4">How It Works</h2>
          <p className="text-center">Our AI-powered tool analyzes your goals and interests to create a tailored 4-year plan to guide you through college and beyond.</p>
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
                placeholder="e.g., Web Development, AI, Design"
                value={formData.interests}
                onChange={handleChange}
                required
              />
            </div>
            <div className="mb-3">
              <label htmlFor="credits" className="form-label">How many credits per semester?</label>
              <input
                type="number"
                id="credits"
                name="credits"
                className="form-control"
                placeholder="e.g., 15"
                value={formData.credits}
                onChange={handleChange}
                required
              />
            </div>
            <div className="mb-3">
              <label htmlFor="transferCredits" className="form-label">How many transfer credits do you have?</label>
              <input
                type="number"
                id="transferCredits"
                name="transferCredits"
                className="form-control"
                placeholder="e.g., 12"
                value={formData.transferCredits}
                onChange={handleChange}
                required
              />
            </div>
            <div className="mb-3">
              <label htmlFor="completedCourses" className="form-label">Which classes have you already completed?</label>
              <textarea
                id="completedCourses"
                name="completedCourses"
                className="form-control"
                placeholder="e.g., CS101, Math 222"
                value={formData.completedCourses}
                onChange={handleChange}
                required
              ></textarea>
            </div>
            <button type="submit" className="btn btn-primary w-100">Generate Plan</button>
          </form>

          {/* Render Generated Plan */}
          {generatedPlan.length > 0 && (
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
