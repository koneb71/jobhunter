-- Seed admin user
INSERT INTO users (
    email,
    first_name,
    last_name,
    hashed_password,
    user_type,
    is_superuser
) VALUES (
    'admin@jobhunter.com',
    'Admin',
    'User',
    -- Default password is 'admin123' - change in production
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',
    'employer',
    true
) ON CONFLICT (email) DO NOTHING;

-- Seed test company
INSERT INTO companies (
    name,
    description,
    website,
    industry,
    size,
    founded_year,
    headquarters,
    employer_id
) VALUES (
    'JobHunter Inc.',
    'Leading job search platform connecting talented professionals with great companies.',
    'https://jobhunter.com',
    'Technology',
    '50-100',
    2024,
    'San Francisco, CA',
    (SELECT id FROM users WHERE email = 'admin@jobhunter.com')
) ON CONFLICT DO NOTHING;

-- Seed test job
INSERT INTO jobs (
    title,
    description,
    company_id,
    location,
    job_type,
    experience_level,
    salary_min,
    salary_max,
    salary_currency,
    is_remote,
    required_skills,
    preferred_skills,
    benefits,
    is_featured,
    posted_by
) VALUES (
    'Senior Full Stack Developer',
    'We are looking for an experienced Full Stack Developer to join our growing team...',
    (SELECT id FROM companies WHERE name = 'JobHunter Inc.'),
    'San Francisco, CA',
    'full_time',
    'senior',
    120000,
    180000,
    'USD',
    true,
    ARRAY['JavaScript', 'Python', 'React', 'Node.js', 'PostgreSQL'],
    ARRAY['TypeScript', 'AWS', 'Docker', 'Kubernetes'],
    ARRAY['Health Insurance', '401(k)', 'Remote Work', 'Flexible Hours', 'Professional Development'],
    true,
    (SELECT id FROM users WHERE email = 'admin@jobhunter.com')
) ON CONFLICT DO NOTHING; 