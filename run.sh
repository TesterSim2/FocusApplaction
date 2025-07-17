#!/bin/bash
# Startup script for Focus AI

# Activate virtual environment
source venv/bin/activate

# Check for required models
python -c "import spacy; spacy.load('en_core_web_sm')" || python -m spacy download en_core_web_sm

# Run the application
streamlit run app.py --server.port 8501 --server.address localhost
