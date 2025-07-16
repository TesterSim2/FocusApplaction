"""Tool Management and Integration System"""

import requests
import json
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class Tool(ABC):
    """Base class for all tools"""
    
    @abstractmethod
    def execute(self, query: str, parameters: Dict = None) -> Dict:
        """Execute the tool with given parameters"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Get tool description"""
        pass

class SearchTool(Tool):
    """Web search tool implementation"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        
    def execute(self, query: str, parameters: Dict = None) -> Dict:
        """Execute web search"""
        # Simulate search results
        return {
            'results': [
                {'title': f'Result 1 for {query}', 'snippet': 'Sample snippet 1'},
                {'title': f'Result 2 for {query}', 'snippet': 'Sample snippet 2'}
            ],
            'status': 'success'
        }
    
    def get_description(self) -> str:
        return "Search the web for current information"

class CalculatorTool(Tool):
    """Mathematical calculation tool"""
    
    def execute(self, query: str, parameters: Dict = None) -> Dict:
        """Execute calculation"""
        try:
            # Safe evaluation of mathematical expressions
            result = eval(query, {"__builtins__": {}}, 
                         {"sin": np.sin, "cos": np.cos, "sqrt": np.sqrt})
            return {'result': result, 'status': 'success'}
        except Exception as e:
            return {'error': str(e), 'status': 'error'}
    
    def get_description(self) -> str:
        return "Perform mathematical calculations"

class ChartTool(Tool):
    """Data visualization tool"""
    
    def execute(self, query: str, parameters: Dict = None) -> Dict:
        """Create charts and visualizations"""
        # Parse parameters for chart type and data
        chart_type = parameters.get('type', 'line')
        data = parameters.get('data', {})
        
        # Create simple visualization
        fig, ax = plt.subplots()
        
        if chart_type == 'line':
            ax.plot(data.get('x', []), data.get('y', []))
        elif chart_type == 'bar':
            ax.bar(data.get('x', []), data.get('y', []))
        
        # Save to buffer
        from io import BytesIO
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        
        return {
            'chart': buffer,
            'type': chart_type,
            'status': 'success'
        }
    
    def get_description(self) -> str:
        return "Create charts and data visualizations"

class ToolManager:
    """Manages all available tools"""
    
    def __init__(self):
        self.tools = {
            'search': SearchTool(),
            'calculator': CalculatorTool(),
            'chart': ChartTool()
        }
        
    def execute_tool(self, tool_name: str, query: str, parameters: Dict = None) -> Dict:
        """Execute a specific tool"""
        if tool_name not in self.tools:
            return {'error': f'Tool {tool_name} not found', 'status': 'error'}
        
        return self.tools[tool_name].execute(query, parameters)
    
    def get_available_tools(self) -> Dict[str, str]:
        """Get all available tools and their descriptions"""
        return {
            name: tool.get_description() 
            for name, tool in self.tools.items()
        }
    
    def suggest_tools(self, query: str) -> List[str]:
        """Suggest tools based on the query"""
        suggestions = []
        
        # Simple keyword-based suggestions
        if any(word in query.lower() for word in ['search', 'find', 'look up']):
            suggestions.append('search')
        
        if any(word in query.lower() for word in ['calculate', 'compute', 'math']):
            suggestions.append('calculator')
        
        if any(word in query.lower() for word in ['chart', 'graph', 'plot', 'visualize']):
            suggestions.append('chart')
        
        return suggestions
