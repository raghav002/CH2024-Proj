import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min'; // Import Bootstrap's JS bundle for dropdown functionality
import React, { useState } from 'react';
import './App.css';

const App = () => {
  const [formData, setFormData] = useState({ major: '', goals: '' });
  const [generatedPlan, setGeneratedPlan] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const plan = `
      <h3>Your 4-Year Plan:</h3>
      <p><strong>Major:</strong> ${formData.major}</p>
      <p><strong>Goals:</strong> ${formData.goals}</p>
      <p>Year 1: Focus on foundational courses in ${formData.major}. Set a study routine. Start exploring extracurriculars.</p>
      <p>Year 2: Dive deeper into advanced subjects. Network with professors. Start internships.</p>
      <p>Year 3: Begin to specialize. Focus on personal development. Prepare for your capstone project or thesis.</p>
      <p>Year 4: Finish your degree with strong achievements. Prepare for post-graduation career opportunities.</p>
    `;
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
              <label htmlFor="major" className="form-label">What is your major?</label>
              <input
                type="text"
                id="major"
                name="major"
                className="form-control"
                placeholder="Enter your major"
                value={formData.major}
                onChange={handleChange}
                required
              />
            </div>
            <div className="mb-3">
              <label htmlFor="goals" className="form-label">What are your goals for the next 4 years?</label>
              <textarea
                id="goals"
                name="goals"
                className="form-control"
                placeholder="Academic, personal, or career goals..."
                value={formData.goals}
                onChange={handleChange}
                required
              ></textarea>
            </div>
            <button type="submit" className="btn btn-primary w-100">Generate Plan</button>
          </form>

          {generatedPlan && (
            <div
              id="generatedPlan"
              className="p-4 bg-white border rounded shadow"
              dangerouslySetInnerHTML={{ __html: generatedPlan }}
            ></div>
          )}
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="py-5">
        <div className="container">
          <h2 className="text-center mb-4">Contact Us</h2>
          <p className="text-center">If you have any questions or need support, feel free to reach out!</p>
          <form>
            <div className="mb-3">
              <label htmlFor="email" className="form-label">Your Email</label>
              <input
                type="email"
                id="email"
                name="email"
                className="form-control"
                placeholder="Enter your email"
                required
              />
            </div>
            <div className="mb-3">
              <textarea
                name="message"
                className="form-control"
                placeholder="Your message"
                required
              ></textarea>
            </div>
            <button type="submit" className="btn btn-success w-100">Send Message</button>
          </form>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-primary text-white text-center py-3">
        <p>&copy; 2024 Your 4-Year Plan. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default App;
