# PortfolioAI

A modern, AI-powered portfolio generator that helps users create professional portfolios and resumes with ease, built with Streamlit and FastAPI.

## 🌟 Features

- **AI-Powered Portfolio Generation**: Generate professional portfolios using AI
- **Resume Builder**: Create and optimize your resume
- **Cover Letter Generator**: Generate personalized cover letters
- **User Authentication**: Secure user accounts and data management
- **Streamlit UI**: Interactive and user-friendly interface

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Streamlit (will be installed via requirements)

### Project Structure

```
PortfolioAI/
├── backend/         # FastAPI backend service
│   ├── app/         # Main application code
│   └── ...
├── frontend/        # Streamlit frontend application
│   ├── src/         # Source code
│   └── ...
├── docs/           # Project documentation
├── requirements.txt # Global dependencies
└── README.md       # This file
```

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd PortfolioAI
   ```

2. **Set up a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy example environment files
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   
   # Update the variables in both .env files with your configuration
   ```

5. **Run the application**
   - Start the backend:
     ```bash
     cd backend
     python run.py
     ```
   - In a new terminal, start the frontend:
     ```bash
     cd frontend
     streamlit run app.py
     ```
   - The application should now be running at `http://localhost:8501`

## 📚 Documentation

- [Backend API Documentation](/backend/README.md)
- [Frontend Documentation](/frontend/README.md)
- [Deployment Guide](/docs/DEPLOYMENT.md)

## 🛠 Built With

- **Frontend**: Streamlit (Python web framework)
- **Backend**: FastAPI (Python API framework)
- **Database**: SQLAlchemy (ORM), SQLite (development)
- **AI/ML**: 
  - NLP models for content generation
  - Integration with AI services
- **Authentication**: JWT (JSON Web Tokens)
- **Templating**: Jinja2
- **Document Processing**: python-docx, PyPDF2

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to all contributors who have helped shape this project.
