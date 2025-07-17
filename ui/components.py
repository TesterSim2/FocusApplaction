"""Streamlit UI Components for Focus AI"""

import streamlit as st
from typing import Dict
import pandas as pd


def render_sidebar(components: Dict):
    """Render the main sidebar"""
    st.sidebar.markdown("# 🎯 Focus AI")
    st.sidebar.markdown("*Next-Level AI Interaction*")

    tabs = {
        'chat': '💬 Chat',
        'focus': '🎯 Focus Mode',
        'rag': '📚 RAG',
        'agents': '🤖 Agents',
        'settings': '⚙️ Settings'
    }

    selected_tab = st.sidebar.radio(
        "Navigation",
        options=list(tabs.keys()),
        format_func=lambda x: tabs[x],
        key='tab_selector'
    )
    st.session_state.current_tab = selected_tab

    st.sidebar.markdown("---")
    st.sidebar.subheader("AI Mode")
    mode = st.sidebar.select_slider(
        "Response Style",
        options=['precise', 'balanced', 'creative'],
        value=st.session_state.get('ai_mode', 'balanced')
    )
    st.session_state.ai_mode = mode

    st.sidebar.markdown("---")
    st.sidebar.subheader("🛠️ Active Tools")
    tools = ['🔍 Search', '🧮 Calculator', '📊 Charts', '📝 Notes']
    for tool in tools:
        st.sidebar.checkbox(tool, value=True)

    st.sidebar.markdown("---")
    st.sidebar.metric("Messages", len(st.session_state.get('messages', [])))
    st.sidebar.metric("Certainty Avg", f"{85}%")

    render_sidebar_focus_ring()


def render_sidebar_focus_ring():
    """Render a mini focus ring in sidebar"""
    import plotly.graph_objects as go

    fig = go.Figure()
    for i in range(3):
        fig.add_shape(
            type="circle",
            x0=-1-i*0.1, y0=-1-i*0.1,
            x1=1+i*0.1, y1=1+i*0.1,
            line=dict(color=f"rgba(78,205,196,{0.3-i*0.1})", width=2),
            fillcolor=f"rgba(78,205,196,{0.1-i*0.03})"
        )

    fig.update_layout(
        showlegend=False,
        height=100,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False, range=[-2, 2]),
        yaxis=dict(visible=False, range=[-2, 2]),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.sidebar.plotly_chart(fig, use_container_width=True)


def render_chat_message(message: Dict):
    """Render a single chat message"""
    if message['role'] == 'user':
        with st.container():
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(
                    f"""<div class="user-message">
                    {message['content']}
                    </div>""",
                    unsafe_allow_html=True
                )
            with col2:
                st.caption(message['timestamp'].strftime("%I:%M %p"))
    else:
        with st.container():
            col1, col2 = st.columns([1, 5])
            with col1:
                st.caption(message['timestamp'].strftime("%I:%M %p"))
            with col2:
                st.markdown(
                    f"""<div class="ai-message">
                    {message['content']}
                    </div>""",
                    unsafe_allow_html=True
                )
                if 'certainty' in message:
                    render_mini_certainty_bar(message['certainty']['score'])
                if message.get('tools_used'):
                    st.caption(f"🛠️ Used: {', '.join(message['tools_used'])}")


def render_mini_certainty_bar(score: float):
    """Render a small certainty indicator"""
    color = '#6bcf7f' if score > 0.7 else '#ffd93d' if score > 0.4 else '#ff6b6b'
    st.markdown(
        f"""<div style="height: 4px; width: {score*100}%; 
        background: {color}; border-radius: 2px; margin-top: 8px;">
        </div>""",
        unsafe_allow_html=True
    )


def render_focus_ring():
    """Render the main focus ring animation"""
    st.markdown(
        """
    <div class="focus-ring-container">
        <div class="focus-ring"></div>
        <div class="focus-ring" style="animation-delay: 0.5s;"></div>
        <div class="focus-ring" style="animation-delay: 1s;"></div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_task_contextualization(components):
    """Render task contextualization interface"""
    st.subheader("📋 Task Contextualization")
    task_types = [
        "Text Analysis", "Code Generation", "Research",
        "Creative Writing", "Data Analysis", "Problem Solving"
    ]
    selected_tasks = st.multiselect(
        "Select task types for your query:",
        task_types
    )
    if selected_tasks:
        st.write("### Task-Specific Instructions")
        for task in selected_tasks:
            with st.expander(f"{task} Settings"):
                if task == "Code Generation":
                    st.selectbox("Language", ["Python", "JavaScript", "Java", "C++"])
                    st.selectbox("Style", ["Clean", "Optimized", "Commented"])
                elif task == "Research":
                    st.slider("Research Depth", 1, 10, 5)
                    st.multiselect("Source Types", ["Academic", "News", "Blogs"])


def render_deep_research(components):
    """Render deep research interface"""
    st.subheader("🔬 Deep Research Mode")
    research_topic = st.text_area(
        "Research Topic",
        placeholder="Enter a topic for comprehensive research..."
    )
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Maximum Sources", 5, 50, 20)
        st.selectbox("Time Range", ["Last Week", "Last Month", "Last Year", "All Time"])
    with col2:
        st.select_slider(
            "Research Depth",
            options=["Surface", "Standard", "Deep", "Exhaustive"],
            value="Standard",
        )
        st.checkbox("Include contrarian viewpoints")
    if st.button("🚀 Start Deep Research", type="primary"):
        with st.spinner("Conducting deep research..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            steps = [
                "Creating research plan...",
                "Searching primary sources...",
                "Analyzing academic papers...",
                "Cross-referencing data...",
                "Synthesizing findings...",
            ]
            for i, step in enumerate(steps):
                status_text.text(step)
                progress_bar.progress((i + 1) / len(steps))
            st.success("Research complete!")
            st.markdown("### Research Findings")
            tabs = st.tabs(["Summary", "Sources", "Analysis", "Visualizations"])
            with tabs[0]:
                st.write("**Key Findings:**")
                st.write("1. Primary insight from research")
                st.write("2. Supporting evidence")
                st.write("3. Contradictory viewpoints")
            with tabs[1]:
                st.write("**Sources Analyzed:** 23")
                sources_df = pd.DataFrame({
                    'Source': ['Paper 1', 'Article 2', 'Study 3'],
                    'Relevance': [0.95, 0.87, 0.82],
                    'Date': ['2024', '2024', '2023']
                })
                st.dataframe(sources_df)


def render_personas_manager(components):
    """Render AI personas management interface"""
    st.subheader("🎭 AI Personas")
    with st.expander("Create New Persona"):
        col1, col2 = st.columns(2)
        with col1:
            persona_name = st.text_input("Persona Name")
            persona_role = st.selectbox(
                "Role",
                ["Expert", "Creative", "Analyst", "Teacher", "Researcher"],
            )
        with col2:
            expertise = st.multiselect(
                "Areas of Expertise",
                ["Technology", "Science", "Business", "Arts", "Philosophy"],
            )
            personality = st.select_slider(
                "Personality",
                options=["Formal", "Balanced", "Casual"],
                value="Balanced",
            )
        if st.button("Create Persona"):
            if persona_name:
                if 'personas' not in st.session_state:
                    st.session_state.personas = {}
                st.session_state.personas[persona_name] = {
                    'role': persona_role,
                    'expertise': expertise,
                    'personality': personality,
                    'created': datetime.now(),
                }
                st.success(f"Created persona: {persona_name}")
    if 'personas' in st.session_state and st.session_state.personas:
        st.write("### Your Personas")
        for name, details in st.session_state.personas.items():
            with st.expander(f"🎭 {name} - {details['role']}"):
                st.write(f"**Expertise:** {', '.join(details['expertise'])}")
                st.write(f"**Personality:** {details['personality']}")
                st.write(f"**Created:** {details['created'].strftime('%Y-%m-%d')}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Chat with {name}", key=f"chat_{name}"):
                        st.session_state.active_persona = name
                        st.session_state.current_tab = 'chat'
                        st.rerun()
                with col2:
                    if st.button(f"Delete {name}", key=f"del_{name}"):
                        del st.session_state.personas[name]
                        st.rerun()


def render_gauntlet_system(components):
    """Render the Gauntlet debate system"""
    st.subheader("⚔️ The Gauntlet - Multi-Perspective Debate")
    debate_topic = st.text_area(
        "Debate Topic",
        placeholder="Enter a complex topic for multi-perspective analysis...",
    )
    chairs = {
        "The Skeptic": "Questions assumptions and seeks evidence",
        "The Visionary": "Explores possibilities and future potential",
        "The Pragmatist": "Focuses on practical implementation",
        "The Devil's Advocate": "Argues contrarian viewpoints",
        "The Synthesizer": "Finds common ground and integration",
    }
    selected_chairs = st.multiselect(
        "Select debate participants:",
        list(chairs.keys()),
        default=list(chairs.keys())[:3],
    )
    debate_rounds = st.slider("Debate Rounds", 1, 5, 3)
    if st.button("⚔️ Start Debate", type="primary"):
        if debate_topic and selected_chairs:
            with st.spinner("Debate in progress..."):
                for round_num in range(debate_rounds):
                    st.write(f"### Round {round_num + 1}")
                    for chair in selected_chairs:
                        with st.expander(f"{chair}'s Perspective"):
                            st.write(f"*{chairs[chair]}*")
                            st.write(f"[{chair} would provide their analysis here...]")
                st.write("### 🏆 Final Synthesis")
                st.info("After considering all perspectives, the key insights are...")


def render_focus_group_results(result):
    """Display focus group session results"""
    st.success("Focus Group Session Complete!")
    st.write("### Participants")
    participants_df = pd.DataFrame(result.participants)
    st.dataframe(participants_df)
    st.write("### Discussion Rounds")
    for round_data in result.rounds:
        with st.expander(f"Round {round_data['round']}"):
            st.write(f"**Overseer Notes:** {round_data['overseer_notes']}")
            for participant_id, response in round_data['responses'].items():
                st.write(f"**{participant_id}:** {response['content'][:200]}...")
    st.write("### Final Synthesis")
    st.info(result.final_synthesis)
    st.metric("Overall Confidence", f"{result.confidence:.1%}")
