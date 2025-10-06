# AI-Powered SQL Query Assistant

An intelligent SQL query generation system that converts natural language questions into executable SQL queries using Large Language Models (Google Gemini). This tool enables non-technical users to interact with databases through conversational interfaces without knowing SQL syntax.

## Project Overview

The AI SQL Assistant bridges the gap between natural language and database queries, allowing users to ask questions in plain English and receive accurate SQL queries along with their results. The system uses Google's Gemini LLM for natural language understanding and query generation, with built-in safety checks to prevent malicious or destructive operations.

## Key Features

- **Natural Language to SQL Conversion** - Ask questions in plain English, get optimized SQL queries
- **Real-time Query Execution** - Execute generated queries and view results instantly
- **Security-First Architecture** - Multiple layers of validation to prevent SQL injection and destructive operations
- **Interactive Web Interface** - User-friendly Streamlit UI with modern design
- **RESTful API** - FastAPI backend for easy integration with other applications
- **Schema-Aware Generation** - Understands database structure for accurate query generation
- **Read-Only Safety** - Enforces SELECT-only queries, blocks DML/DDL operations
- **Query Result Limiting** - Automatic pagination to prevent performance issues

## Technology Stack

**Backend:**
- FastAPI - High-performance API framework
- SQLAlchemy - Database ORM and query execution
- Google Gemini AI - Large Language Model for NL-to-SQL conversion
- SQLParse - SQL query parsing and validation
- Python-dotenv - Environment configuration management

**Frontend:**
- Streamlit - Interactive web application framework
- HTTPX - Async HTTP client for API communication

**Database:**
- SQLite - Lightweight database for demonstration
- Compatible with PostgreSQL, MySQL, and other SQL databases

## Project Structure

```
ai-sql-assistant/
├── backend/
│   ├── __init__.py
│   ├── db.py              # Database connection & safety checks
│   └── llm.py             # LLM integration (Gemini API)
├── frontend/
│   └── streamlit_app.py   # Streamlit UI
├── app.py                 # FastAPI backend
├── create_sample_db.py    # Sample database creation
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- Git (for cloning the repository)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/ai-sql-assistant.git
cd ai-sql-assistant
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**

Create a `.env` file in the project root:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=sqlite:///./sample.db
```

To get your Gemini API key:
- Go to https://makersuite.google.com/app/apikey
- Create a new API key
- Copy and paste it into your `.env` file

5. **Create sample database:**
```bash
python create_sample_db.py
```

This will create a SQLite database with sample customers and orders data.

### Running the Application

#### Option 1: Full Stack (Recommended)

**Terminal 1 - Start Backend:**
```bash
uvicorn app:app --reload --port 8000
```

**Terminal 2 - Start Frontend:**
```bash
streamlit run frontend/streamlit_app.py
```

Access the application at: `http://localhost:8501`

#### Option 2: API Only

```bash
uvicorn app:app --reload --port 8000
```

API documentation available at: `http://localhost:8000/docs`

## Usage Examples

### Sample Database Schema

The sample database includes:
```sql
customers(id, name, email, city)
orders(id, customer_id, amount, order_date, status)
```

### Example Queries

**Basic Queries:**
- "Show all customers from Karachi"
- "List all orders from 2023"
- "What is the total number of customers?"

**Aggregation Queries:**
- "Which customers spent the most in 2023?"
- "Calculate average order amount by city"
- "Count total orders per customer"

**Complex Queries:**
- "Find customers with orders over $500 who live in Lahore"
- "Show top 5 customers by total spending"
- "List customers with only completed orders"

### API Usage

**Request:**
```json
POST http://localhost:8000/query
{
  "question": "Which customers spent the most in 2023?",
  "schema": "customers(id, name, email, city)\norders(id, customer_id, amount, order_date, status)",
  "max_results": 200
}
```

**Response:**
```json
{
  "sql": "SELECT c.name, SUM(o.amount) as total_spent FROM customers c JOIN orders o ON c.id = o.customer_id WHERE o.order_date LIKE '2023%' GROUP BY c.name ORDER BY total_spent DESC",
  "columns": ["name", "total_spent"],
  "rows": [
    {"name": "Alice Johnson", "total_spent": 421.49},
    {"name": "Bob Malik", "total_spent": 475.00}
  ]
}
```

## Security Features

### Multi-Layer Query Validation

1. **Keyword Filtering** - Blocks dangerous SQL operations:
   - DROP, DELETE, ALTER, INSERT, UPDATE
   - CREATE, REPLACE, TRUNCATE, GRANT, REVOKE

2. **Query Structure Validation**
   - Ensures queries start with SELECT
   - Uses SQLParse for syntax validation
   - Removes SQL injection vectors

3. **Result Limiting**
   - Automatic LIMIT clause injection
   - Configurable maximum row returns
   - Prevents resource exhaustion

4. **Read-Only Enforcement**
   - Database permissions restricted to SELECT
   - No data modification capabilities
   - Safe for production database connections

## Configuration

### Environment Variables

```bash
# Required
GEMINI_API_KEY=your_api_key_here

# Optional
DATABASE_URL=sqlite:///./sample.db  # Default database
BACKEND_URL=http://localhost:8000   # API endpoint for frontend
```

### Connecting to Your Own Database

To use your own database instead of the sample:

1. **Update `.env` file:**
```bash
# For PostgreSQL
DATABASE_URL=postgresql://user:password@localhost/dbname

# For MySQL
DATABASE_URL=mysql://user:password@localhost/dbname

# For SQL Server
DATABASE_URL=mssql+pyodbc://user:password@localhost/dbname?driver=ODBC+Driver+17+for+SQL+Server
```

2. **Provide your schema in the UI**

## System Architecture

### Components

1. **LLM Module (`backend/llm.py`)**
   - Integrates with Google Gemini API
   - Converts natural language to SQL using prompt engineering
   - Handles edge cases and invalid queries

2. **Database Module (`backend/db.py`)**
   - Manages database connections via SQLAlchemy
   - Implements security validation for SQL queries
   - Blocks forbidden keywords
   - Enforces query limits

3. **API Layer (`app.py`)**
   - RESTful endpoints for query generation and execution
   - Request/response validation using Pydantic models
   - Error handling and HTTP status management

4. **Frontend (`frontend/streamlit_app.py`)**
   - Modern, responsive UI with gradient themes
   - Real-time query generation and execution
   - Interactive schema input and result visualization

## Troubleshooting

### Common Issues

**1. "GEMINI_API_KEY not set in .env"**
- Make sure you created a `.env` file in the project root
- Verify the API key is correct
- Don't use quotes around the key value

**2. "Module not found" errors**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

**3. "Backend not responding"**
- Check if backend is running on port 8000
- Verify no other service is using port 8000
- Check firewall settings

**4. "Database not found"**
- Run `python create_sample_db.py` to create the database
- Check DATABASE_URL in `.env` file

## Development

### Adding New Features

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/AmazingFeature`
3. Make your changes
4. Test thoroughly
5. Commit: `git commit -m 'Add some AmazingFeature'`
6. Push: `git push origin feature/AmazingFeature`
7. Open a Pull Request

### Testing

To test the API endpoints:
```bash
# Using curl
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "Show all customers", "schema": "customers(id, name, email, city)"}'
```

## Future Enhancements

- Multi-database support (PostgreSQL, MySQL, SQL Server)
- Query history and favorites
- Export results to CSV/Excel
- Query optimization suggestions
- Data visualization integration
- User authentication
- Query caching for performance
- Support for CTEs and window functions

## Dependencies

```
fastapi==0.95.2
uvicorn[standard]==0.22.0
google-generativeai
sqlalchemy==2.0.20
pandas==2.2.3
sqlparse==0.5.4
python-dotenv==1.0.0
streamlit==1.24.1
httpx==0.24.0
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

**Hassan Iqbal**
- GitHub: [@Hasssaan514](https://github.com/Hasssaan514)

## Acknowledgments

- Google Gemini AI for natural language processing
- FastAPI for excellent API framework
- Streamlit for rapid UI development
- SQLAlchemy for robust database management

---

**Built with AI, Python, and Modern Web Technologies**
