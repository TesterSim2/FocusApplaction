"""Persistent Memory Management System"""

import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional
import numpy as np
from sentence_transformers import SentenceTransformer

class MemoryManager:
    """Manages conversation memory and knowledge persistence"""
    
    def __init__(self, db_path: str = "focus_ai_memory.db"):
        self.db_path = db_path
        self.encoder = None  # Initialize sentence transformer lazily
        self._init_db()
        
    def _init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                timestamp DATETIME,
                user_message TEXT,
                ai_response TEXT,
                context TEXT,
                metadata TEXT
            )
        ''')
        
        # Knowledge base table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                content TEXT,
                embedding BLOB,
                timestamp DATETIME,
                source TEXT
            )
        ''')
        
        # User preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS preferences (
                user_id TEXT PRIMARY KEY,
                preferences TEXT,
                updated_at DATETIME
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def store_conversation(self, session_id: str, user_msg: str, 
                         ai_response: str, context: Dict = None):
        """Store a conversation exchange"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO conversations (session_id, timestamp, user_message, 
                                     ai_response, context, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            session_id,
            datetime.now().isoformat(),
            user_msg,
            ai_response,
            json.dumps(context) if context else '{}',
            '{}'
        ))
        
        conn.commit()
        conn.close()
    
    def retrieve_similar_conversations(self, query: str, limit: int = 5) -> List[Dict]:
        """Retrieve similar past conversations"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Simple retrieval - in production, use vector similarity
        cursor.execute('''
            SELECT * FROM conversations 
            WHERE user_message LIKE ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (f'%{query}%', limit))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'user_message': r[3],
                'ai_response': r[4],
                'timestamp': r[2],
                'context': json.loads(r[5])
            }
            for r in results
        ]
    
    def update_user_preferences(self, user_id: str, preferences: Dict):
        """Update user preferences"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO preferences (user_id, preferences, updated_at)
            VALUES (?, ?, ?)
        ''', (
            user_id,
            json.dumps(preferences),
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
