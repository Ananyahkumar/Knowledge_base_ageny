# Knowledge Base Agent (RAG + LLaMA)

## Overview of the Agent

The Knowledge Base Agent is a Retrieval-Augmented Generation (RAG) system that enables users to interact with PDF documents through natural language queries. The agent processes PDF files locally, creates a vector-based knowledge base, and answers questions using an offline LLaMA model (Phi-3) via Ollama.

The system is designed to work entirely **offline** after initial setup, ensuring data privacy and eliminating dependency on cloud-based APIs for core functionality. Questions and answers are automatically logged to Google Sheets for tracking and analysis.

### How It Works

1. **Document Ingestion**: Users upload a PDF file through the Streamlit interface
2. **Text Extraction**: PDF content is extracted using `pdfplumber`
3. **Chunking**: Text is split into overlapping chunks for optimal retrieval
4. **Vectorization**: Chunks are embedded using sentence transformers and stored in ChromaDB
5. **Query Processing**: User queries are embedded and matched against the vector store
6. **Answer Generation**: Retrieved context is passed to Ollama (Phi-3 model) to generate answers
7. **Logging**: Questions and answers are logged to Google Sheets

## Features & Limitations

### Features

- ✅ **Offline Processing**: Complete local processing with no dependency on cloud APIs (except Google Sheets logging)
- ✅ **PDF Document Support**: Upload and process PDF documents seamlessly
- ✅ **RAG Architecture**: Retrieval-Augmented Generation for accurate, context-aware answers
- ✅ **Local LLM**: Uses Ollama with Phi-3 model for private, fast inference
- ✅ **Vector Search**: Semantic search using ChromaDB and sentence transformers
- ✅ **User-Friendly Interface**: Intuitive Streamlit web interface
- ✅ **Question Logging**: Automatic logging to Google Sheets for analytics
- ✅ **Persistent Storage**: Vector database persists between sessions

### Limitations

- ⚠️ **Single Document**: Processes one PDF at a time (previous documents are overwritten)
- ⚠️ **Ollama Dependency**: Requires Ollama to be installed and running locally
- ⚠️ **Model Availability**: Depends on having Phi-3 model installed in Ollama
- ⚠️ **Chunking Strategy**: Simple word-based chunking (200 words, 50 overlap) may not preserve document structure
- ⚠️ **Context Window**: Limited to 1200 characters of context per query
- ⚠️ **No Multi-document Support**: Cannot query across multiple documents simultaneously
- ⚠️ **Fixed Retrieval**: Retrieves only top 2 chunks (k=2) per query
- ⚠️ **No Conversation History**: Each query is treated independently
- ⚠️ **Google Sheets Required**: Requires Google Cloud service account credentials for logging

## Tech Stack & APIs Used

### Core Technologies

- **Python 3.x**: Programming language
- **Streamlit**: Web application framework for the user interface
- **LangChain**: Framework for building LLM applications and chains
- **ChromaDB**: Open-source vector database for storing embeddings
- **Ollama**: Local LLM runtime for running Phi-3 model
- **Sentence Transformers**: Embedding model (all-MiniLM-L6-v2) for text vectorization

### Libraries & Frameworks

- **pdfplumber**: PDF text extraction
- **langchain-community**: Community integrations for LangChain
- **langchain-openai**: OpenAI integrations (installed but not actively used)
- **python-dotenv**: Environment variable management
- **tqdm**: Progress bars
- **google-api-python-client**: Google Sheets API integration
- **google-auth**: Google authentication
- **google-auth-oauthlib**: OAuth2 library for Google services

### APIs & Services

- **Google Sheets API v4**: For logging questions and answers
  - Requires service account credentials (`gcp_key.json`)
  - Spreadsheet ID and sheet name must be configured

### Models

- **Embedding Model**: `all-MiniLM-L6-v2` (Sentence Transformers)
  - Lightweight, fast, offline embedding model
  - 384-dimensional vectors
- **LLM Model**: `phi3` (via Ollama)
  - Microsoft Phi-3 mini model
  - Runs locally without internet connection

## Setup & Run Instructions

### Prerequisites

1. **Python 3.8+** installed on your system
2. **Ollama** installed and running
   - Download from: https://ollama.ai
   - Install the Phi-3 model: `ollama pull phi3`
3. **Google Cloud Service Account** credentials (for Sheets logging)
   - Create a service account in Google Cloud Console
   - Download the JSON key file
   - Share your Google Sheet with the service account email

### Installation Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd "D:\Internship\Rooman Internship\Challenge"
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - **Windows (PowerShell):**
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **Windows (Command Prompt):**
     ```cmd
     venv\Scripts\activate.bat
     ```
   - **Linux/Mac:**
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure Google Sheets (Optional - for logging)**
   - Place your Google Cloud service account JSON key file as `gcp_key.json` in the project root
   - Update `SHEET_ID` and `SHEET_NAME` in `sheets_logger.py` if needed
   - Share your Google Sheet with the service account email address

6. **Update Ollama Path (if needed)**
   - Open `qa_service.py`
   - Update `OLLAMA_PATH` variable (line 13) with your Ollama executable path
   - Default: `r"C:\Users\anany\AppData\Local\Programs\Ollama\ollama.exe"`

7. **Verify Ollama and Phi-3 model**
   ```bash
   ollama list
   # Should show phi3 in the list
   ```

### Running the Application

1. **Start the Streamlit application**
   ```bash
   streamlit run app.py
   ```

2. **Access the web interface**
   - The application will open in your default browser
   - Default URL: `http://localhost:8501`

3. **Use the application**
   - Click "Browse files" to upload a PDF document
   - Wait for the document to be processed and indexed
   - Enter your question in the text input
   - Click "Ask" to get an answer

### Troubleshooting

- **Ollama not found**: Ensure Ollama is installed and the path in `qa_service.py` is correct
- **Phi-3 model missing**: Run `ollama pull phi3` to download the model
- **ChromaDB errors**: Delete the `chroma_db` folder and re-index your document
- **Google Sheets errors**: Check that `gcp_key.json` exists and the sheet is shared with the service account
- **Encoding errors**: The application is configured for UTF-8 encoding; ensure your PDF contains readable text

## Potential Improvements

### Short-term Enhancements

1. **Multi-document Support**
   - Allow uploading and querying multiple PDFs simultaneously
   - Implement document source attribution in answers

2. **Improved Chunking Strategy**
   - Use semantic chunking based on document structure
   - Implement sliding window with better overlap handling
   - Preserve document metadata (page numbers, sections)

3. **Enhanced Retrieval**
   - Make `k` (number of chunks) configurable
   - Implement hybrid search (keyword + semantic)
   - Add re-ranking of retrieved chunks

4. **Conversation History**
   - Maintain chat history across queries
   - Enable follow-up questions with context
   - Add conversation export functionality

5. **Better Context Management**
   - Dynamically adjust context window based on query complexity
   - Implement context summarization for long documents

### Medium-term Improvements

6. **Advanced UI Features**
   - Show retrieved source chunks with answers
   - Display confidence scores
   - Add document preview and navigation
   - Implement dark mode

7. **Model Flexibility**
   - Support multiple Ollama models (configurable)
   - Add model comparison feature
   - Allow custom prompt templates

8. **Performance Optimization**
   - Implement caching for frequent queries
   - Add batch processing for multiple documents
   - Optimize vector database queries

9. **Export & Sharing**
   - Export Q&A logs to CSV/JSON
   - Generate PDF reports with Q&A sessions
   - Share knowledge bases between users

### Long-term Improvements

10. **Production Features**
    - Add user authentication
    - Implement rate limiting
    - Add error monitoring and logging
    - Deploy as a web service

11. **Advanced RAG Techniques**
    - Implement query expansion and rewriting
    - Add parent document retrieval
    - Use graph-based retrieval for complex queries

12. **Integration Capabilities**
    - API endpoints for programmatic access
    - Webhook support for external integrations
    - Slack/Discord bot integration

13. **Analytics Dashboard**
    - Query analytics and insights
    - Most asked questions tracking
    - Document usage statistics

14. **Document Management**
    - Document versioning support
    - Update/delete documents from knowledge base
    - Document organization and tagging

---

## Project Structure

```
Challenge/
├── app.py                 # Main Streamlit application
├── ingest.py              # PDF processing and chunking
├── vector_store.py        # ChromaDB vector store management
├── qa_service.py          # QA chain with Ollama integration
├── sheets_logger.py       # Google Sheets logging
├── requirements.txt       # Python dependencies
├── gcp_key.json          # Google Cloud service account key (not in repo)
├── chroma_db/            # Persistent vector database directory
└── README.md             # This file
```

## License

This project is part of an internship challenge. Please refer to your organization's policies for licensing and usage terms.

---


