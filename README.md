# Focus AI - Next-Level AI Interaction Platform

A production-ready AI platform built with Streamlit that implements advanced features for AI interaction, including certainty determination, prompt grounding, multi-agent collaboration, and more.

## Features

- 🎯 **Focus Mode**: Deep work with multi-step workflows and task contextualization
- 🤖 **AI Agents**: Focus Group (Roundtable) system and persistent personas
- 📚 **RAG System**: Document management and knowledge base integration
- 🧠 **Certainty Analysis**: Real-time analysis of prompt clarity and helpfulness
- ✨ **Prompt Enhancement**: Automatic prompt grounding and rewriting
- 🛠️ **Integrated Tools**: Search, calculator, charts, and data analysis
- 🎨 **Beautiful UI**: Animated focus rings and modern design

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd focus-ai
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download spaCy model:
```bash
python -m spacy download en_core_web_sm
```

## Configuration

1. Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
```

2. Configure settings in the app or via the Settings tab

## Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Project Structure

```
focus-ai/
├── app.py              # Main Streamlit application
├── core/               # Core AI modules
│   ├── ai_orchestrator.py
│   ├── prompt_processor.py
│   ├── certainty_analyzer.py
│   ├── focus_group.py
│   ├── memory_manager.py
│   └── tool_manager.py
├── ui/                 # UI components
│   ├── components.py
│   └── styles.py
├── data/              # Data storage
├── models/            # Model storage
├── requirements.txt
└── README.md
```

## Usage Guide

### Chat Mode
- Standard AI chat with enhanced features
- Toggle grounding for more accurate responses
- Use the enhance button to improve your prompts
- View certainty scores for each interaction

### Focus Mode
- Build multi-step workflows
- Configure task-specific settings
- Run deep research on any topic

### Agents
- Create and manage AI personas
- Run Focus Group sessions for complex problems
- Use the Gauntlet for multi-perspective debates

### RAG
- Upload and process documents
- Build your knowledge base
- Query documents with AI assistance

## Development

To extend Focus AI:

1. Add new tools in `core/tool_manager.py`
2. Create new UI components in `ui/components.py`
3. Implement new AI features in `core/ai_orchestrator.py`

## License

MIT License - see LICENSE file for details
