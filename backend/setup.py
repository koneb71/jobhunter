from setuptools import setup, find_packages

setup(
    name="jobhunter",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0",
        "sqlalchemy>=1.4.23",
        "alembic>=1.7.1",
        "psycopg2-binary>=2.9.1",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "python-multipart>=0.0.5",
        "pydantic>=2.0.0",
        "pydantic-settings>=2.0.0",
        "python-dotenv>=0.19.0",
    ],
) 