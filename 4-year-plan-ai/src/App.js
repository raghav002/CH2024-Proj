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
      <header>
        <div className="logo">Your 4-Year Plan</div>
        <nav>
          <ul>
            <li><a href="#about">About</a></li>
            <li><a href="#generate">Generate Plan</a></li>
            <li><a href="#contact">Contact</a></li>
          </ul>
        </nav>
      </header>

      <section id="hero">
        <h1>Welcome to Your Personalized 4-Year Plan Powered by AI</h1>
        <p>Let AI help you map out your next four years for academic and professional success!</p>
        <a href="#generate" className="cta-button">Get Started</a>
      </section>

      <section id="about">
        <h2>How It Works</h2>
        <p>Our AI-powered tool analyzes your goals and interests to create a tailored 4-year plan to guide you through college, career growth, and personal development.</p>
      </section>

      <section id="generate">
        <h2>Generate Your Plan</h2>
        <form onSubmit={handleSubmit}>
          <label htmlFor="major">What is your major?</label>
          <input
            type="text"
            id="major"
            name="major"
            placeholder="Enter your major"
            value={formData.major}
            onChange={handleChange}
            required
          />

          <label htmlFor="goals">What are your goals for the next 4 years?</label>
          <textarea
            id="goals"
            name="goals"
            placeholder="Academic, personal, or career goals..."
            value={formData.goals}
            onChange={handleChange}
            required
          ></textarea>

          <button type="submit" className="cta-button">Generate Plan</button>
        </form>

        {generatedPlan && (
          <div
            id="generatedPlan"
            dangerouslySetInnerHTML={{ __html: generatedPlan }}
          ></div>
        )}
      </section>

      <section id="contact">
        <h2>Contact Us</h2>
        <p>If you have any questions or need support, feel free to reach out!</p>
        <form>
          <label htmlFor="email">Your Email</label>
          <input
            type="email"
            id="email"
            name="email"
            placeholder="Enter your email"
            required
          />
          <textarea name="message" placeholder="Your message" required></textarea>
          <button type="submit" className="cta-button">Send Message</button>
        </form>
      </section>

      <footer>
        <p>&copy; 2024 Your 4-Year Plan. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default App;
