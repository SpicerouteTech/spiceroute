from setuptools import setup, find_packages

setup(
    name="auth-service",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.95.2",
        "uvicorn==0.22.0",
        "motor==3.1.1",
        "pymongo==4.3.3",
        "elasticsearch==7.17.9",
        "python-dotenv==0.21.1",
        "pydantic==1.10.7",
        "email-validator==1.3.1",
        "python-jose[cryptography]==3.3.0",
        "python-dateutil==2.8.2",
        "httpx==0.24.1",
        "passlib[bcrypt]==1.7.4",
        "python-multipart==0.0.6",
    ],
    extras_require={
        "dev": [
            "pytest==7.3.1",
            "pytest-asyncio==0.21.0",
            "pytest-cov==4.1.0",
        ],
    },
    python_requires=">=3.7,<4.0",
) 