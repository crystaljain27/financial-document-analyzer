# Financial Document Analyzer

A comprehensive financial document analysis system that processes corporate reports, financial statements, and investment documents using AI-powered analysis agents built with CrewAI.

## Features

- **PDF Document Analysis**: Upload and analyze financial PDF documents
- **AI-Powered Financial Analysis**: Extract key metrics, trends, and insights
- **Investment Recommendations**: Get data-driven buy/hold/sell recommendations
- **Risk Assessment**: Comprehensive risk analysis with mitigation strategies
- **REST API**: Easy-to-use FastAPI endpoints for integration

## Bugs Fixed

### 1. agents.py

#### Bug 1.1: LLM Not Initialized
**Issue**: Line 12 had `llm = llm` which is a reference to an undefined variable.
**Fix**: Properly initialized the LLM using `ChatOpenAI` from `langchain_openai`:
```python
llm = ChatOpenAI(
    model_name=os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini"),
    temperature=0.2,
    api_key=os.getenv("OPENAI_API_KEY")
)
```

#### Bug 1.2: Incorrect Import
**Issue**: `from crewai.agents import Agent` is incorrect.
**Fix**: Changed to `from crewai import Agent`.

#### Bug 1.3: Wrong Parameter Name
**Issue**: Line 28 used `tool=[...]` (singular) instead of `tools=[...]` (plural).
**Fix**: Changed to `tools=[FinancialDocumentTool.read_data_tool]`.

#### Bug 1.4: Inefficient/Sarcastic Prompts
**Issue**: All agent prompts were sarcastic, unprofessional, and instructed the AI to "make up" information.
**Fix**: Rewrote all prompts to be professional, data-driven, and focused on accurate analysis:
- **Financial Analyst**: Now provides rigorous financial analysis based on actual data
- **Verifier**: Properly validates financial documents
- **Investment Advisor**: Provides evidence-based investment recommendations
- **Risk Assessor**: Conducts comprehensive risk analysis

#### Bug 1.5: Missing Tools for Some Agents
**Issue**: `verifier`, `investment_advisor`, and `risk_assessor` agents didn't have tools assigned.
**Fix**: Added `tools=[FinancialDocumentTool.read_data_tool]` to all agents that need to read documents.

#### Bug 1.6: Missing Memory Parameter
**Issue**: `investment_advisor` and `risk_assessor` were missing `memory=True`.
**Fix**: Added `memory=True` to both agents.

### 2. tools.py

#### Bug 2.1: Incorrect Import
**Issue**: `from crewai_tools import tools` was incorrect.
**Fix**: Changed to `from crewai_tools import tool` (singular, the decorator).

#### Bug 2.2: Missing PDF Loader Import
**Issue**: `Pdf` class was used but never imported (line 24).
**Fix**: Added `from langchain_community.document_loaders import PyPDFLoader` and updated the code to use `PyPDFLoader`.

#### Bug 2.3: Async Methods in Tools
**Issue**: Tool methods were defined as `async` which is not compatible with CrewAI tools.
**Fix**: Changed all tool methods to synchronous functions with proper `@tool` decorator.

#### Bug 2.4: Missing Tool Decorators
**Issue**: Tool methods weren't decorated with `@tool`.
**Fix**: Added `@tool("Tool Name")` decorator to all tool methods with proper type hints.

#### Bug 2.5: Inefficient String Processing
**Issue**: Investment tool used inefficient while loop with index manipulation for removing double spaces.
**Fix**: Simplified to use `while "  " in processed_data: processed_data = processed_data.replace("  ", " ")`.

### 3. task.py

#### Bug 3.1: Inefficient/Sarcastic Task Descriptions
**Issue**: All task descriptions and expected outputs were sarcastic and instructed the AI to make up information.
**Fix**: Rewrote all task descriptions and expected outputs to be professional and focused on actual analysis:
- **analyze_financial_document**: Now provides structured financial analysis
- **investment_analysis**: Provides proper investment recommendations
- **risk_assessment**: Conducts thorough risk analysis
- **verification**: Properly validates documents

#### Bug 3.2: Wrong Agent Assignments
**Issue**: All tasks were assigned to `financial_analyst` instead of specialized agents.
**Fix**: Updated task assignments:
- `investment_analysis` → `investment_advisor`
- `risk_assessment` → `risk_assessor`
- `verification` → `verifier`

#### Bug 3.3: Missing Search Tool
**Issue**: Tasks that could benefit from web search didn't have the `search_tool`.
**Fix**: Added `search_tool` to tasks where additional market context would be helpful.

### 4. main.py

#### Bug 4.1: File Path Not Passed to Crew
**Issue**: The `run_crew` function received `file_path` parameter but didn't pass it to `kickoff()`.
**Fix**: Updated `kickoff()` call to include `file_path`:
```python
result = financial_crew.kickoff({'query': query, 'file_path': file_path})
```

#### Bug 4.2: Function Name Conflict
**Issue**: The endpoint function `analyze_financial_document` had the same name as the imported task.
**Fix**: Renamed the endpoint function to `analyze_document`.

### 5. requirements.txt

#### Bug 5.1: Missing Dependencies
**Issue**: Several required packages were missing:
- `pypdf` - For PDF processing
- `uvicorn` - For running the FastAPI server
- `python-dotenv` - For environment variable management
- `python-multipart` - For file uploads in FastAPI
- `langchain-openai` - For ChatOpenAI LLM
- `langchain-community` - For PyPDFLoader

**Fix**: Added all missing dependencies to requirements.txt.

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- OpenAI API key

### Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd financial-document-analyzer
```

2. **Create a virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL_NAME=gpt-4o-mini  # Optional, defaults to gpt-4o-mini
```

### Running the Application

1. **Start the server**:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

2. **Access the API**:
- API will be available at: `http://localhost:8000`
- Interactive API docs (Swagger UI): `http://localhost:8000/docs`
- Alternative API docs (ReDoc): `http://localhost:8000/redoc`

## API Documentation

### Endpoints

#### 1. Health Check
```http
GET /
```

**Response**:
```json
{
  "message": "Financial Document Analyzer API is running"
}
```

#### 2. Analyze Financial Document
```http
POST /analyze
```

**Content-Type**: `multipart/form-data`

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file | File | Yes | PDF file to analyze |
| query | String | No | Analysis query/prompt (default: "Analyze this financial document for investment insights") |

**Example Request**:
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "accept: application/json" \
  -F "file=@TSLA-Q2-2025-Update.pdf" \
  -F "query=Analyze Tesla's Q2 2025 financial performance and provide investment recommendations"
```

**Example Response**:
```json
{
  "status": "success",
  "query": "Analyze Tesla's Q2 2025 financial performance and provide investment recommendations",
  "analysis": "... detailed analysis content ...",
  "file_processed": "TSLA-Q2-2025-Update.pdf"
}
```

**Error Response** (500):
```json
{
  "detail": "Error processing financial document: [error message]"
}
```

## Architecture

### Agents

1. **Financial Analyst** (`financial_analyst`)
   - Role: Senior Financial Analyst
   - Purpose: Extract key financial metrics and trends from documents
   - Tools: Financial document reader

2. **Document Verifier** (`verifier`)
   - Role: Financial Document Verifier
   - Purpose: Validate uploaded documents are proper financial documents
   - Tools: Financial document reader

3. **Investment Advisor** (`investment_advisor`)
   - Role: Investment Advisor
   - Purpose: Provide investment recommendations based on analysis
   - Tools: Financial document reader, search tool

4. **Risk Assessor** (`risk_assessor`)
   - Role: Risk Assessment Specialist
   - Purpose: Identify and assess investment risks
   - Tools: Financial document reader, search tool

### Tasks

1. **analyze_financial_document**: Comprehensive financial analysis
2. **investment_analysis**: Investment recommendation generation
3. **risk_assessment**: Risk analysis and mitigation strategies
4. **verification**: Document validation

### Tools

1. **FinancialDocumentTool.read_data_tool**: Reads and extracts text from PDF files
2. **search_tool**: SerperDevTool for web search (market context)

## Sample Document

The repository includes Tesla's Q2 2025 financial update (`data/TSLA-Q2-2025-Update.pdf`) for testing purposes.

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | - | Your OpenAI API key |
| `OPENAI_MODEL_NAME` | No | gpt-4o-mini | OpenAI model to use |
| `SERPER_API_KEY` | No | - | API key for Serper search tool (optional) |

## Bonus Features Implemented

### Enhanced Architecture
- Proper agent specialization with dedicated roles
- Professional, data-driven prompts
- Comprehensive error handling

### Code Quality
- Type hints for better code clarity
- Proper async/sync handling
- Clean, maintainable code structure

## License

This project is part of a debugging assignment for VWO AI Internship.
