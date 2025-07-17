# Focus AI - Production-Ready Streamlit Application
# File: app.py (Main Application)

import streamlit as st
import asyncio
from datetime import datetime
import json
import os
from typing import Dict, List, Optional, Any
import pandas as pd
import plotly.graph_objects as go
from dataclasses import dataclass, asdict
import numpy as np

# Import our custom modules
from core.ai_orchestrator import AIOrchestrator
from core.prompt_processor import PromptProcessor
from core.certainty_analyzer import CertaintyAnalyzer
from core.focus_group import FocusGroupSystem
from core.memory_manager import MemoryManager
from core.tool_manager import ToolManager
from ui.components import (
    render_sidebar,
    render_chat_message,
    render_focus_ring,
    render_task_contextualization,
    render_deep_research,
    render_personas_manager,
    render_gauntlet_system,
    render_focus_group_results,
)
from ui.styles import load_custom_css

# Page configuration
st.set_page_config(
    page_title="Focus AI - Next-Level AI Interaction",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
load_custom_css()

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        'messages': [],
        'current_tab': 'chat',
        'ai_mode': 'balanced',
        'conversation_context': [],
        'attached_files': [],
        'grounding_enabled': False,
        'current_workflow': None,
        'ai_personas': {},
        'focus_group_active': False,
        'certainty_threshold': 0.7,
        'memory_bank': {},
        'tool_results': {},
        'thinking_visible': False,
        'api_keys': {}
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Initialize components
@st.cache_resource
def init_components():
    """Initialize AI components"""
    return {
        'orchestrator': AIOrchestrator(),
        'prompt_processor': PromptProcessor(),
        'certainty_analyzer': CertaintyAnalyzer(),
        'focus_group': FocusGroupSystem(),
        'memory_manager': MemoryManager(),
        'tool_manager': ToolManager()
    }

def main():
    """Main application entry point"""
    init_session_state()
    components = init_components()
    
    # Custom CSS injection
    st.markdown("""
    <style>
    /* Main container styling */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Focus Ring Animation */
    @keyframes focusRing {
        0% { transform: scale(0.95); opacity: 0.5; }
        50% { transform: scale(1.05); opacity: 0.8; }
        100% { transform: scale(0.95); opacity: 0.5; }
    }
    
    .focus-ring {
        position: absolute;
        width: 100%;
        height: 100%;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(78,205,196,0.3) 0%, transparent 70%);
        animation: focusRing 3s ease-in-out infinite;
    }
    
    /* Message styling */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 1rem;
        margin: 0.5rem 0;
        max-width: 70%;
        margin-left: auto;
    }
    
    .ai-message {
        background: #ffffff;
        color: #2d3748;
        padding: 1rem;
        border-radius: 1rem;
        margin: 0.5rem 0;
        max-width: 70%;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Certainty indicator */
    .certainty-bar {
        height: 4px;
        background: linear-gradient(to right, #ff6b6b, #ffd93d, #6bcf7f);
        border-radius: 2px;
        margin-top: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        render_sidebar(components)
    
    # Main content area based on selected tab
    if st.session_state.current_tab == 'chat':
        render_chat_tab(components)
    elif st.session_state.current_tab == 'focus':
        render_focus_tab(components)
    elif st.session_state.current_tab == 'rag':
        render_rag_tab(components)
    elif st.session_state.current_tab == 'agents':
        render_agents_tab(components)
    elif st.session_state.current_tab == 'settings':
        render_settings_tab()

def render_chat_tab(components):
    """Render the main chat interface"""
    st.title("🎯 Focus AI Chat")
    
    # Display conversation
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            render_chat_message(msg)
    
    # Input area
    col1, col2 = st.columns([6, 1])
    
    with col1:
        # Multi-line input with dynamic height
        user_input = st.text_area(
            "Message Focus AI...",
            height=100,
            key="chat_input",
            placeholder="Type your message or describe what you need..."
        )
    
    with col2:
        st.write("") # Spacing
        send_button = st.button("🚀 Send", use_container_width=True)
        
        # Tool buttons
        with st.expander("🛠️ Tools"):
            if st.button("🔍 Ground"):
                st.session_state.grounding_enabled = not st.session_state.grounding_enabled
            
            if st.button("✨ Enhance"):
                if user_input:
                    enhanced = components['prompt_processor'].enhance_prompt(user_input)
                    st.session_state.enhanced_prompt = enhanced
                    st.info(f"Enhanced: {enhanced}")
            
            if st.button("📊 Analyze"):
                if user_input:
                    certainty = components['certainty_analyzer'].analyze(user_input)
                    render_certainty_score(certainty)
    
    # Process message
    if send_button and user_input:
        process_message(user_input, components)
    
    # Show thinking space if enabled
    if st.session_state.thinking_visible:
        with st.expander("🧠 AI Thinking Process", expanded=True):
            render_thinking_process()

def render_focus_tab(components):
    """Render the Focus Mode interface"""
    st.title("🎯 Focus Mode - Deep Work")
    
    tab1, tab2, tab3 = st.tabs(["Workflow Builder", "Task Context", "Deep Research"])
    
    with tab1:
        st.subheader("Multi-Step Workflow Builder")
        
        # Workflow steps
        if 'workflow_steps' not in st.session_state:
            st.session_state.workflow_steps = []
        
        # Add step interface
        with st.form("add_step"):
            step_prompt = st.text_area("Step prompt:")
            use_previous = st.checkbox("Use output from previous step")
            tools = st.multiselect("Required tools:", ["Search", "Calculate", "Analyze", "Generate"])
            
            if st.form_submit_button("Add Step"):
                st.session_state.workflow_steps.append({
                    'prompt': step_prompt,
                    'use_previous': use_previous,
                    'tools': tools
                })
        
        # Display workflow
        for i, step in enumerate(st.session_state.workflow_steps):
            with st.expander(f"Step {i+1}: {step['prompt'][:50]}..."):
                st.write(f"Uses previous: {step['use_previous']}")
                st.write(f"Tools: {', '.join(step['tools'])}")
                if st.button(f"Remove Step {i+1}"):
                    st.session_state.workflow_steps.pop(i)
                    st.rerun()
        
        if st.button("🚀 Execute Workflow", type="primary"):
            execute_workflow(components)
    
    with tab2:
        render_task_contextualization(components)
    
    with tab3:
        render_deep_research(components)

def render_agents_tab(components):
    """Render the Agents & Personas interface"""
    st.title("🤖 AI Agents & Personas")
    
    tab1, tab2, tab3 = st.tabs(["Focus Group", "Personas", "The Gauntlet"])
    
    with tab1:
        st.subheader("🎭 Focus Group System (The Roundtable)")
        
        # Focus group configuration
        col1, col2 = st.columns(2)
        with col1:
            participants = st.slider("Number of Participants", 3, 7, 5)
            overseer_mode = st.selectbox("Overseer Style", ["Strict", "Balanced", "Creative"])
        
        with col2:
            judge_threshold = st.slider("Judge Strictness", 0.1, 1.0, 0.7)
            rounds = st.number_input("Review Rounds", 1, 5, 2)
        
        # Input for focus group
        query = st.text_area("Present your question to the Focus Group:")
        
        if st.button("🎯 Convene Focus Group", type="primary"):
            with st.spinner("Focus Group in session..."):
                result = components['focus_group'].run_session(
                    query=query,
                    participants=participants,
                    overseer_mode=overseer_mode,
                    judge_threshold=judge_threshold,
                    rounds=rounds
                )
                render_focus_group_results(result)
    
    with tab2:
        render_personas_manager(components)
    
    with tab3:
        render_gauntlet_system(components)

def render_rag_tab(components):
    """Render the RAG (Retrieval Augmented Generation) interface"""
    st.title("📚 Knowledge Base & RAG")
    
    # File upload section
    st.subheader("📁 Document Management")
    
    uploaded_files = st.file_uploader(
        "Upload documents to your knowledge base",
        type=['pdf', 'txt', 'md', 'docx', 'csv'],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        for file in uploaded_files:
            if st.button(f"Process {file.name}"):
                process_document(file, components)
    
    # Knowledge base viewer
    st.subheader("🗂️ Knowledge Base")
    
    if 'knowledge_base' not in st.session_state:
        st.session_state.knowledge_base = []
    
    for doc in st.session_state.knowledge_base:
        with st.expander(f"📄 {doc['name']}"):
            st.write(f"Type: {doc['type']}")
            st.write(f"Size: {doc['size']} chunks")
            st.write(f"Added: {doc['timestamp']}")
            if st.button(f"Remove {doc['name']}"):
                st.session_state.knowledge_base.remove(doc)
                st.rerun()

def process_message(user_input: str, components: Dict):
    """Process user message with full Focus AI capabilities"""
    
    # Add user message
    user_msg = {
        'role': 'user',
        'content': user_input,
        'timestamp': datetime.now(),
        'mode': st.session_state.ai_mode,
        'grounding': st.session_state.grounding_enabled
    }
    st.session_state.messages.append(user_msg)
    
    # Analyze certainty
    certainty = components['certainty_analyzer'].analyze(user_input)
    
    # Process with grounding if enabled
    if st.session_state.grounding_enabled:
        grounded_prompt = components['prompt_processor'].ground_prompt(user_input)
        processing_prompt = grounded_prompt
    else:
        processing_prompt = user_input
    
    # Get AI response
    with st.spinner("🧠 Focus AI is thinking..."):
        response = components['orchestrator'].process(
            prompt=processing_prompt,
            mode=st.session_state.ai_mode,
            context=st.session_state.conversation_context,
            certainty_threshold=certainty['score']
        )
    
    # Add AI response
    ai_msg = {
        'role': 'assistant',
        'content': response['content'],
        'timestamp': datetime.now(),
        'certainty': certainty,
        'tools_used': response.get('tools_used', []),
        'thinking': response.get('thinking', '')
    }
    st.session_state.messages.append(ai_msg)
    
    # Update conversation context
    st.session_state.conversation_context.append({
        'user': user_input,
        'assistant': response['content'],
        'certainty': certainty['score']
    })
    
    st.rerun()

def render_certainty_score(certainty: Dict):
    """Render certainty analysis visualization"""
    score = certainty['score']
    color = '#6bcf7f' if score > 0.7 else '#ffd93d' if score > 0.4 else '#ff6b6b'
    
    st.metric("Certainty Score", f"{score:.1%}")
    st.progress(score)
    
    with st.expander("Certainty Analysis"):
        st.write(f"**Helpful Probability:** {certainty['helpful_probability']:.1%}")
        st.write(f"**Potential Issues:** {', '.join(certainty['potential_issues'])}")
        st.write(f"**Recommendations:** {certainty['recommendation']}")

def render_thinking_process():
    """Display AI's thinking process"""
    if st.session_state.messages and st.session_state.messages[-1]['role'] == 'assistant':
        thinking = st.session_state.messages[-1].get('thinking', 'No thinking process available')
        st.code(thinking, language='markdown')

def execute_workflow(components):
    """Execute multi-step workflow"""
    with st.spinner("Executing workflow..."):
        results = []
        previous_output = None
        
        for i, step in enumerate(st.session_state.workflow_steps):
            st.write(f"Executing Step {i+1}...")
            
            prompt = step['prompt']
            if step['use_previous'] and previous_output:
                prompt = f"Based on the previous output: {previous_output}\n\n{prompt}"
            
            result = components['orchestrator'].process(
                prompt=prompt,
                tools=step['tools']
            )
            
            results.append(result)
            previous_output = result['content']
            
            # Display intermediate result
            with st.expander(f"Step {i+1} Result"):
                st.write(result['content'])
        
        # Display final result
        st.success("Workflow completed!")
        st.write("### Final Output:")
        st.write(results[-1]['content'])

if __name__ == "__main__":
    main()
