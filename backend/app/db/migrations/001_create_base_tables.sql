-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create enum types
CREATE TYPE user_type AS ENUM ('job_seeker', 'employer');
CREATE TYPE job_type AS ENUM ('full_time', 'part_time', 'contract', 'internship', 'freelance');
CREATE TYPE experience_level AS ENUM ('entry', 'junior', 'mid', 'senior', 'lead', 'executive');
CREATE TYPE application_status AS ENUM ('pending', 'reviewed', 'shortlisted', 'interviewed', 'offered', 'rejected', 'accepted', 'withdrawn');

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    user_type user_type NOT NULL,
    is_active BOOLEAN DEFAULT true,
    is_superuser BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create companies table
CREATE TABLE IF NOT EXISTS companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    website VARCHAR(255),
    industry VARCHAR(100),
    size VARCHAR(50),
    founded_year INTEGER,
    headquarters VARCHAR(255),
    logo_url VARCHAR(255),
    employer_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    is_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create jobs table
CREATE TABLE IF NOT EXISTS jobs (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
    location VARCHAR(255),
    job_type job_type NOT NULL,
    experience_level experience_level NOT NULL,
    salary_min INTEGER,
    salary_max INTEGER,
    salary_currency VARCHAR(3),
    is_remote BOOLEAN DEFAULT false,
    required_skills TEXT[],
    preferred_skills TEXT[],
    benefits TEXT[],
    is_active BOOLEAN DEFAULT true,
    is_featured BOOLEAN DEFAULT false,
    views_count INTEGER DEFAULT 0,
    applications_count INTEGER DEFAULT 0,
    posted_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create job_applications table
CREATE TABLE IF NOT EXISTS job_applications (
    id SERIAL PRIMARY KEY,
    job_id INTEGER REFERENCES jobs(id) ON DELETE CASCADE,
    applicant_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    resume_url VARCHAR(255),
    cover_letter TEXT,
    status application_status DEFAULT 'pending',
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create user_profiles table for additional user information
CREATE TABLE IF NOT EXISTS user_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    headline VARCHAR(255),
    bio TEXT,
    location VARCHAR(255),
    phone VARCHAR(50),
    website VARCHAR(255),
    avatar_url VARCHAR(255),
    skills TEXT[],
    languages TEXT[],
    availability_status VARCHAR(50),
    preferred_job_types job_type[],
    preferred_locations TEXT[],
    expected_salary INTEGER,
    salary_currency VARCHAR(3),
    is_open_to_work BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create education table
CREATE TABLE IF NOT EXISTS education (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    institution VARCHAR(255) NOT NULL,
    degree VARCHAR(255) NOT NULL,
    field_of_study VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    grade FLOAT,
    activities TEXT,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create work_experience table
CREATE TABLE IF NOT EXISTS work_experience (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    company_name VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    start_date DATE NOT NULL,
    end_date DATE,
    is_current BOOLEAN DEFAULT false,
    description TEXT,
    skills_used TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create saved_jobs table for job bookmarks
CREATE TABLE IF NOT EXISTS saved_jobs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    job_id INTEGER REFERENCES jobs(id) ON DELETE CASCADE,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, job_id)
);

-- Create job_alerts table
CREATE TABLE IF NOT EXISTS job_alerts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    keywords TEXT[],
    location VARCHAR(255),
    job_types job_type[],
    experience_levels experience_level[],
    salary_min INTEGER,
    salary_max INTEGER,
    is_remote BOOLEAN,
    frequency VARCHAR(50),
    is_active BOOLEAN DEFAULT true,
    last_sent_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_jobs_company_id ON jobs(company_id);
CREATE INDEX idx_jobs_location ON jobs(location);
CREATE INDEX idx_jobs_type ON jobs(job_type);
CREATE INDEX idx_jobs_experience ON jobs(experience_level);
CREATE INDEX idx_jobs_is_active ON jobs(is_active);
CREATE INDEX idx_jobs_is_featured ON jobs(is_featured);
CREATE INDEX idx_applications_job_id ON job_applications(job_id);
CREATE INDEX idx_applications_applicant_id ON job_applications(applicant_id);
CREATE INDEX idx_applications_status ON job_applications(status);
CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX idx_education_user_id ON education(user_id);
CREATE INDEX idx_work_experience_user_id ON work_experience(user_id);
CREATE INDEX idx_saved_jobs_user_id ON saved_jobs(user_id);
CREATE INDEX idx_job_alerts_user_id ON job_alerts(user_id);

-- Create triggers for updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply update_updated_at trigger to all tables
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_companies_updated_at
    BEFORE UPDATE ON companies
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_jobs_updated_at
    BEFORE UPDATE ON jobs
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_job_applications_updated_at
    BEFORE UPDATE ON job_applications
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_profiles_updated_at
    BEFORE UPDATE ON user_profiles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_education_updated_at
    BEFORE UPDATE ON education
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_work_experience_updated_at
    BEFORE UPDATE ON work_experience
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_job_alerts_updated_at
    BEFORE UPDATE ON job_alerts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Enable Row Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE companies ENABLE ROW LEVEL SECURITY;
ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE job_applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE education ENABLE ROW LEVEL SECURITY;
ALTER TABLE work_experience ENABLE ROW LEVEL SECURITY;
ALTER TABLE saved_jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE job_alerts ENABLE ROW LEVEL SECURITY;

-- Create RLS policies
CREATE POLICY "Users can view their own data" ON users
    FOR ALL
    USING (auth.uid() = id);

CREATE POLICY "Companies are viewable by everyone" ON companies
    FOR SELECT
    USING (true);

CREATE POLICY "Companies are manageable by their owners" ON companies
    FOR ALL
    USING (auth.uid() = employer_id);

CREATE POLICY "Jobs are viewable by everyone" ON jobs
    FOR SELECT
    USING (is_active = true OR auth.uid() = posted_by);

CREATE POLICY "Jobs are manageable by their posters" ON jobs
    FOR ALL
    USING (auth.uid() = posted_by);

CREATE POLICY "Applications are viewable by job poster and applicant" ON job_applications
    FOR SELECT
    USING (
        auth.uid() IN (
            SELECT posted_by FROM jobs WHERE id = job_id
            UNION
            SELECT applicant_id
        )
    );

CREATE POLICY "Applications are manageable by applicants" ON job_applications
    FOR ALL
    USING (auth.uid() = applicant_id);

-- Grant necessary permissions
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO authenticated;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO authenticated; 