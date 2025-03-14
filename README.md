# JobHunter - Professional Job Search Platform

A comprehensive job search platform that connects job seekers with employers, featuring advanced search capabilities, profile verification, and real-time notifications.

## Features

### For Job Seekers
- Advanced job search with filters and AI-powered recommendations
- Professional profile creation with verification badges
- Document upload and management (resumes, certificates)
- Real-time job alerts and notifications
- Application tracking and status updates
- Skill assessment and matching
- Profile visibility controls
- Saved jobs and search preferences

### For Employers
- Job posting and management
- Candidate search and filtering
- Application review and management
- Company profile management
- Verification badge system
- Analytics dashboard
- Bulk candidate communication
- Custom job application forms

### Platform Features
- Real-time notifications system
- Profile verification system
- Document management
- Search optimization
- Mobile-responsive design
- Multi-language support
- Analytics and reporting
- API access for integration

## Tech Stack

### Backend
- FastAPI (Python web framework)
- PostgreSQL (Database)
- SQLAlchemy (ORM)
- Pydantic (Data validation)
- JWT (Authentication)
- Celery (Task queue)
- Redis (Caching)
- AWS S3 (File storage)

### Frontend
- React (UI framework)
- TypeScript
- Tailwind CSS (Styling)
- Redux Toolkit (State management)
- React Query (Data fetching)
- Socket.IO (Real-time features)

## Project Structure

```
jobhunter/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── auth.py
│   │   │   │   ├── users.py
│   │   │   │   ├── jobs.py
│   │   │   │   ├── companies.py
│   │   │   │   ├── applications.py
│   │   │   │   ├── search.py
│   │   │   │   ├── notifications.py
│   │   │   │   └── verification.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── events.py
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   └── session.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── job.py
│   │   │   ├── company.py
│   │   │   ├── application.py
│   │   │   ├── notification.py
│   │   │   └── verification_request.py
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   ├── job.py
│   │   │   ├── company.py
│   │   │   ├── application.py
│   │   │   ├── notification.py
│   │   │   └── verification.py
│   │   └── services/
│   │       ├── auth.py
│   │       ├── user.py
│   │       ├── job.py
│   │       ├── company.py
│   │       ├── application.py
│   │       ├── notification.py
│   │       └── verification.py
│   ├── tests/
│   ├── alembic/
│   ├── requirements.txt
│   └── .env
└── frontend/
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   ├── services/
    │   ├── store/
    │   ├── hooks/
    │   └── utils/
    ├── public/
    ├── package.json
    └── .env
```

## Setup Instructions

### Backend Setup

1. Create and activate virtual environment:
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
# Edit .env with your configuration
```

4. Initialize database:
```bash
alembic upgrade head
```

5. Create a super user:
```bash
python create_admin.py --email admin@example.com --password <password> --first-name Admin --last-name User
```

6. Run development server:
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
# Edit .env with your configuration
```

3. Run development server:
```bash
npm run dev
```

## Development Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use ESLint and Prettier for JavaScript/TypeScript
- Write meaningful commit messages
- Include docstrings for functions and classes

### Testing
- Write unit tests for new features
- Run tests before committing changes
- Maintain test coverage above 80%

### Git Workflow
- Create feature branches from develop
- Use conventional commits
- Submit pull requests for review
- Squash merge to develop

### Documentation
- Update API documentation
- Document new environment variables
- Keep README up to date
- Add inline code comments

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 