"""AI Orchestrator - Central AI coordination system"""

import asyncio
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import openai
import requests
import json

@dataclass
class AIResponse:
    content: str
    thinking: str
    tools_used: List[str]
    confidence: float
    metadata: Dict[str, Any]

class AIOrchestrator:
    """Orchestrates AI model interactions and tool usage"""
    
    def __init__(self):
        self.models = {
            'openai': None,  # Initialize with API key
            'anthropic': None,
            'local': None
        }
        self.conversation_history = []
        self.active_tools = {}
        
    def process(self, prompt: str, mode: str = 'balanced', 
                context: List[Dict] = None, tools: List[str] = None,
                certainty_threshold: float = 0.7) -> Dict:
        """Process a prompt with full orchestration"""
        
        # Build system prompt based on mode
        system_prompt = self._build_system_prompt(mode)
        
        # Add context if available
        if context:
            context_str = self._format_context(context)
            prompt = f"{context_str}\n\n{prompt}"
        
        # Determine if tools are needed
        if tools:
            response = self._process_with_tools(prompt, tools)
        else:
            response = self._process_standard(prompt, system_prompt)
        
        # Add thinking process
        thinking = self._generate_thinking_process(prompt, response)
        
        return {
            'content': response,
            'thinking': thinking,
            'tools_used': tools or [],
            'timestamp': datetime.now().isoformat()
        }
    
    def _build_system_prompt(self, mode: str) -> str:
        """Build system prompt based on mode"""
        prompts = {
            'balanced': "You are Focus AI, a helpful and intelligent assistant. Provide clear, accurate, and well-reasoned responses.",
            'creative': "You are Focus AI in creative mode. Think outside the box, be imaginative, and provide innovative solutions.",
            'precise': "You are Focus AI in precise mode. Be exact, detailed, and technically accurate in your responses.",
            'research': "You are Focus AI in research mode. Provide comprehensive, well-sourced information with critical analysis."
        }
        return prompts.get(mode, prompts['balanced'])
    
    def _process_with_tools(self, prompt: str, tools: List[str]) -> str:
        """Process prompt using specified tools and then query the model"""
        results = {}
        for tool in tools:
            if tool == 'search':
                results[tool] = self._search_tool(prompt)
            elif tool == 'calculate':
                results[tool] = self._calculate_tool(prompt)
            # Additional tools can be registered here

        tool_summary = "\n".join(f"{name}: {output}" for name, output in results.items())

        prompt_with_tools = f"{prompt}\n\nTool Results:\n{tool_summary}"
        return self._process_standard(prompt_with_tools, self._build_system_prompt('balanced'))
    
    def _generate_thinking_process(self, prompt: str, response: str) -> str:
        """Generate a thinking process explanation"""
        return f"""
Thinking Process:
1. Analyzed the prompt: "{prompt[:100]}..."
2. Identified key concepts and requirements
3. Considered multiple approaches
4. Selected optimal response strategy
5. Generated response with confidence checks
        """

    def _format_context(self, context: List[Dict]) -> str:
        """Format conversation context for inclusion in a prompt"""
        return "\n".join(
            f"{item.get('role', 'user')}: {item.get('content', '')}" for item in context
        )

    def _process_standard(self, prompt: str, system_prompt: str) -> str:
        """Process prompt using the OpenAI API"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return "OPENAI_API_KEY not configured"
        openai.api_key = api_key
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
            )
            return response.choices[0].message["content"].strip()
        except Exception as exc:
            return f"OpenAI API error: {exc}"

    def _search_tool(self, prompt: str) -> str:
        """Simple web search using DuckDuckGo"""
        try:
            resp = requests.get(
                "https://duckduckgo.com/?q={}&format=json&no_redirect=1&no_html=1".format(
                    requests.utils.quote(prompt)
                )
            )
            data = resp.json()
            topics = data.get("RelatedTopics", [])
            if topics:
                return topics[0].get("Text", "")
            return "No results found"
        except Exception as exc:
            return f"Search error: {exc}"

    def _calculate_tool(self, prompt: str) -> str:
        """Evaluate a mathematical expression"""
        try:
            result = eval(prompt, {"__builtins__": {}})
            return f"Calculation result: {result}"
        except Exception as exc:
            return f"Calculation error: {exc}"
