# IP Consulting Project

API for IPv4 and IPv6 address lookup using Redis cache and local BIN databases.

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Redis (Optional, system works without it using local BINs)

### Installation
1. Clone the repository.
2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   .\env\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the API
From the `src` directory:
```bash
cd src
uvicorn app.main:app --reload
```

## 🏗️ Architecture
- **src/app**: FastAPI application and configuration.
- **src/repository**: Data access layer for Redis and BIN files.
- **src/user_case**: Business logic and validation.
- **src/namespace.py**: Unified import system using absolute paths from `src/`.

## ✅ Validation Layer
- **API level**: Input validation using FastAPI Query parameters.
- **Use Case level**: Strict IP format validation using `ipaddress` module.
- **Data level**: Verifies the integrity of records retrieved from databases.

## 🧪 Testing
Run the complete test suite from the project root:
```bash
$env:PYTHONPATH = "c:\Users\etejada\Downloads\ip_consultig"; python -m pytest src/tests
```

### Included Tests:
- `test_validation.py`: IP format and logic validation.
- `test_connection.py`: Database and cache connectivity.
- `test_integration.py`: API endpoint integration tests.

## 🛠️ Infrastructure
- **infra/docker**: Dockerfiles for containerization.
- **ci-cd**: Basic CI/CD pipeline definitions.
