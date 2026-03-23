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
- **src/repository**: Data access layer for Redis and BIN files. Optimized with `mget`/`mset` and pipelines for bulk operations.
- **src/user_case**: Business logic and validation. Includes `GetBulkIPInfoUseCase` for high-performance concurrent lookups.
- **src/namespace.py**: Unified import system using absolute paths from `src/`.

## 🔌 API Endpoints

### Single IP Lookup
- **GET** `/get-ip?ip=<ip_address>`
- Returns information for a single IP.

### Bulk IP Lookup (High Performance)
- **POST** `/get-ips`
- **Body**: `{ "ips": ["ip1", "ip2", ...] }`
- Features:
  - **Deduplication**: Avoids redundant lookups for duplicate IPs in the list.
  - **Bulk Cache**: Uses Redis `MGET` to fetch multiple records in a single round-trip.
  - **Concurrency**: Parallelizes BIN file lookups using `ThreadPoolExecutor` (max 10 workers).
  - **Bulk Storage**: Uses Redis pipelines to save new results efficiently.

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

## ⚖️ License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Attribution
This project uses IP2Location LITE data available from [https://lite.ip2location.com](https://lite.ip2location.com).
The database is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/).
