# JobHunter - Comprehensive Job Search Platform

A modern job search platform built with FastAPI, Supabase, and React + Vite + TailwindCSS.

## Features

### For Job Seekers
- User registration and profile management
- Detailed profile creation with work experience, education, and skills
- Resume upload and management
- Advanced job search with filters
- One-click apply functionality
- Application status tracking
- Real-time notifications

### For Employers
- Company registration and profile management
- Rich company profiles with media and branding
- Job posting management
- Application management dashboard
- Integrated messaging system
- Interview scheduling tools
- Analytics dashboard

### Platform Features
- Real-time notifications
- Secure payment integration
- API support for third-party integrations
- SEO optimization
- Multilingual support
- Community engagement features
- Career resources and discussion forums

## Tech Stack

### Backend
- FastAPI (Python web framework)
- Supabase (Database, Authentication, Storage)
- PostgreSQL (Primary database)
- Redis (Caching and real-time features)

### Frontend
- React + Vite
- TailwindCSS
- TypeScript
- React Query
- React Router
- Zustand (State management)

## Project Structure

```
jobhunter/
├── backend/           # FastAPI backend
│   ├── app/          # Application code
│   ├── tests/        # Backend tests
│   └── requirements.txt
├── frontend/         # React frontend
│   ├── src/         # Source code
│   ├── public/      # Static assets
│   └── package.json
└── README.md
```

## Setup Instructions

### Backend Setup
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your Supabase credentials
   ```

4. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup
1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API endpoints
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

## Development Guidelines

- Follow PEP 8 style guide for Python code
- Use ESLint and Prettier for frontend code formatting
- Write unit tests for critical functionality
- Use conventional commits for version control
- Follow GitFlow branching strategy

## License

MIT License 