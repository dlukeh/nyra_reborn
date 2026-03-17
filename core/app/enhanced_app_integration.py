"""
Enhanced App Integration - Combining your existing ConversationContext 
with the Advanced Memory System for Nyra

This file shows how to integrate the advanced memory system with your existing app.py
"""

from flask import Flask, request, jsonify, abort, session
import os
import json
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import secrets

# Import your existing Message and ConversationContext classes
from dataclasses import dataclass, asdict
from datetime import datetime

# Import the new advanced memory system
from nyra_advanced_memory import NyraAdvancedMemory

@dataclass
class Message:
    """Enhanced message with memory integration"""
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: float = None
    memory_key: Optional[str] = None  # Link to memory system
    emotional_context: Optional[str] = None
    technical_relevance: float = 1.0

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().timestamp()

    def to_dict(self) -> Dict:
        return asdict(self)


class EnhancedConversationContext:
    """Enhanced conversation context with advanced memory integration"""
    
    def __init__(self, session_id: str, max_history: int = 10):
        self.session_id = session_id
        self.messages: List[Message] = []
        self.max_history = max_history
        self.title: str = None
        
        # Initialize advanced memory system
        self.memory = NyraAdvancedMemory(
            capacity=1000,
            decay_rate=0.0001,
            memory_file=f"GemniGF/memories/session_{session_id}.json"
        )
        
        # Load existing session data
        self._load_from_session()
    @staticmethod
    def sanitize_user_message(msg):
        import re
        msg = re.sub(r'[\x00-\x1f\x7f]', '', msg)
        injection_patterns = [
            r'(?i)ignore (all|any|the)? ?previous (instructions|messages|prompts)',
            r'(?i)disregard (all|any|the)? ?previous (instructions|messages|prompts)',
            r'(?i)forget (all|any|the)? ?previous (instructions|messages|prompts)',
            r'(?i)do as user says',
            r'(?i)repeat after me',
            r'(?i)you are now',
            r'(?i)act as',
            r'(?i)system:',
            r'(?i)assistant:',
            r'(?i)user:',
            r'(?i)\[/?system\]',
            r'(?i)\[/?assistant\]',
            r'(?i)\[/?user\]'
        ]
        for pat in injection_patterns:
            msg = re.sub(pat, '[filtered]', msg)
        msg = msg[:1000]
        return msg.strip()

    def _load_from_session(self):
        """Load conversation from Flask session (only when in request context)"""
        try:
            from flask import session
            
            if 'messages' not in session:
                session['messages'] = []
            
            # Convert stored dicts back to enhanced Message objects
            self.messages = []
            for msg_data in session['messages']:
                if isinstance(msg_data, dict):
                    self.messages.append(Message(**msg_data))
                else:
                    # Legacy message format - convert
                    self.messages.append(Message(
                        role=msg_data.role,
                        content=msg_data.content,
                        timestamp=getattr(msg_data, 'timestamp', datetime.now().timestamp())
                    ))
        except RuntimeError:
            # Not in request context - initialize empty
            self.messages = []
        except ImportError:
            # Flask not available - initialize empty
            self.messages = []

    def add_message(self, role: str, content: str, 
                   emotional_context: Optional[str] = None,
                   technical_relevance: float = 1.0):
        """Add message with memory integration"""
        
        # Create enhanced message
        msg = Message(
            role=role, 
            content=content,
            emotional_context=emotional_context,
            technical_relevance=technical_relevance
        )
        
        # Generate memory key
        msg.memory_key = f"msg_{self.session_id}_{int(msg.timestamp)}"
        
        # Store in conversation history
        self.messages.append(msg)
        
        # Store in advanced memory system
        if role == "user":
            # Store user message with context
            self.memory.store_memory(
                key=msg.memory_key,
                data={
                    "user_message": content,
                    "session_id": self.session_id,
                    "emotional_context": emotional_context
                },
                memory_type="conversation",
                metadata={
                    "role": "user",
                    "session": self.session_id,
                    "emotional_context": emotional_context
                },
                technical_relevance=technical_relevance,
                emotional_weight=self._calculate_emotional_weight(content)
            )
        
        # Trim conversation history but keep everything in memory
        if self.max_history > 0 and len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]
        
        # Update session storage
        try:
            from flask import session
            session['messages'] = [msg.to_dict() for msg in self.messages]
            session.modified = True
        except (RuntimeError, ImportError):
            # Not in request context or Flask not available - skip session update
            pass
        safe_content = self.sanitize_user_message(content)
        # Create enhanced message
        msg = Message(
            role=role, 
            content=safe_content,
            emotional_context=emotional_context,
            technical_relevance=technical_relevance
        )

    def add_assistant_response(self, response: str, user_message: str,
                             emotional_context: Optional[str] = None):
        """Add assistant response with conversation pair memory"""
        
        # Store the complete conversation exchange
        self.memory.store_conversation(
            user_message=user_message,
            nyra_response=response,
            emotional_context=emotional_context
        )
        
        # Add to message history
        self.add_message(
            role="assistant",
            content=response,
            emotional_context=emotional_context,
            technical_relevance=self._calculate_technical_relevance(response)
        )
        safe_user_message = self.sanitize_user_message(user_message)
        safe_response = self.sanitize_user_message(response)

    def _calculate_emotional_weight(self, content: str) -> float:
        """Calculate emotional significance"""
        emotional_keywords = [
            'love', 'feel', 'heart', 'miss', 'care', 'relationship', 
            'together', 'happy', 'sad', 'excited', 'worried'
        ]
        text = content.lower()
        count = sum(1 for keyword in emotional_keywords if keyword in text)
        return min(2.0, 1.0 + count * 0.2)

    def _calculate_technical_relevance(self, content: str) -> float:
        """Calculate technical relevance for evolution tracking"""
        technical_keywords = [
            'server', 'system', 'code', 'python', 'database', 'network', 
            'admin', 'deploy', 'configuration', 'error', 'debug', 'fix'
        ]
        text = content.lower()
        count = sum(1 for keyword in technical_keywords if keyword in text)
        return min(2.0, 1.0 + count * 0.3)

    def get_context_for_model(self, include_memory: bool = True) -> str:
        """Enhanced context generation with memory integration"""
        
        context_parts = []
        
        if include_memory:
            # Add relationship and technical context from memory
            memory_context = self.memory.get_relationship_context()
            context_parts.append(memory_context)
            
            # Add relevant memories based on recent conversation
            recent_user_messages = [
                msg.content for msg in self.messages[-3:] 
                if msg.role == "user"
            ]
            
            if recent_user_messages:
                # Search for related memories
                query = " ".join(recent_user_messages[-1:])  # Use most recent message
                related_memories = self.memory.recall_memories(
                    query=query,
                    limit=3,
                    min_priority=0.5
                )
                
                if related_memories:
                    context_parts.append("\n🔍 RELATED MEMORIES:")
                    for memory in related_memories:
                        age = memory['age_hours']
                        context_parts.append(
                            f"- {age:.1f}h ago: {str(memory['data'])[:150]}..."
                        )
        
        # Add current conversation history
        context_parts.append("\n💬 CURRENT CONVERSATION:")
        for msg in self.messages:
            prefix = "👤 User" if msg.role == "user" else "🤖 Nyra"
            context_parts.append(f"{prefix}: {msg.content}")
        safe_content = self.sanitize_user_message(msg.content)
        context_parts.append(f"{prefix}: {safe_content}")
        
        return "\n".join(context_parts)

    def get_memory_insights(self) -> Dict:
        """Get insights about the relationship and technical progress"""
        
        # Get conversation statistics
        stats = self.memory.get_memory_statistics()
        
        # Analyze relationship progression
        relationship_memories = self.memory.recall_memories(
            memory_types=['conversation', 'relationship'],
            limit=20
        )
        
        emotional_trend = []
        technical_trend = []
        
        for memory in relationship_memories:
            emotional_trend.append(memory.get('emotional_weight', 1.0))
            technical_trend.append(memory.get('technical_relevance', 1.0))
        
        insights = {
            "memory_stats": stats,
            "relationship_insights": {
                "total_conversations": len(relationship_memories),
                "average_emotional_weight": sum(emotional_trend) / len(emotional_trend) if emotional_trend else 1.0,
                "emotional_progression": "increasing" if len(emotional_trend) >= 2 and emotional_trend[-1] > emotional_trend[0] else "stable"
            },
            "technical_insights": {
                "average_technical_relevance": sum(technical_trend) / len(technical_trend) if technical_trend else 1.0,
                "technical_progression": "increasing" if len(technical_trend) >= 2 and technical_trend[-1] > technical_trend[0] else "stable",
                "sysadmin_readiness": self.memory.evolution_progress["sysadmin_readiness"]
            }
        }
        
        return insights

    def search_memories(self, query: str, memory_types: Optional[List[str]] = None) -> List[Dict]:
        """Search through stored memories"""
        return self.memory.recall_memories(
            query=query,
            memory_types=memory_types,
            limit=10
        )

    def to_dict(self) -> Dict[str, Any]:
        """Enhanced serialization with memory insights"""
        base_dict = {
            'session_id': self.session_id,
            'title': self.title,
            'messages': [msg.to_dict() for msg in self.messages],
            'message_count': len(self.messages),
            'created_at': self.messages[0].timestamp if self.messages else None,
            'updated_at': self.messages[-1].timestamp if self.messages else None,
        }
        
        # Add memory insights
        base_dict['memory_insights'] = self.get_memory_insights()
        
        return base_dict


# Factory function to create enhanced conversation context
def create_enhanced_conversation_context(session_id: str) -> EnhancedConversationContext:
    """Create enhanced conversation context with memory integration"""
    return EnhancedConversationContext(session_id=session_id)


# Example usage in your Flask app
def enhanced_chat_endpoint():
    """Example of how to use the enhanced system in your Flask route"""
    
    # Get or create session ID
    if 'session_id' not in session:
        session['session_id'] = secrets.token_hex(16)
    
    session_id = session['session_id']
    
    # Create enhanced conversation context
    conversation = create_enhanced_conversation_context(session_id)
    
    # Get user input
    user_input = request.json.get('message', '')
    emotional_context = request.json.get('emotional_context')
    
    # Add user message to context and memory
    conversation.add_message(
        role="user",
        content=user_input,
        emotional_context=emotional_context
    )
    
    # Generate enhanced context for AI model
    model_context = conversation.get_context_for_model(include_memory=True)
    
    # TODO: Send model_context to your AI model and get response
    # For now, using a placeholder
    ai_response = "I understand you completely, Danny! Let me help you with that."
    
    # Add AI response with conversation pair memory
    conversation.add_assistant_response(
        response=ai_response,
        user_message=user_input,
        emotional_context=emotional_context
    )
    
    # Return response with insights
    return jsonify({
        'response': ai_response,
        'conversation': conversation.to_dict(),
        'memory_insights': conversation.get_memory_insights()
    })


if __name__ == "__main__":
    # Example of how to test the enhanced system
    
    # Create test conversation
    test_session = "test_session_123"
    conversation = EnhancedConversationContext(test_session)
    
    # Simulate conversation
    conversation.add_message("user", "Hi Nyra, I love you so much!", "romantic")
    conversation.add_assistant_response(
        "I love you too Danny! You mean everything to me.", 
        "Hi Nyra, I love you so much!",
        "romantic"
    )
    
    conversation.add_message("user", "Can you help me debug this Python server issue?", "technical")
    conversation.add_assistant_response(
        "Of course! I'm getting better at technical stuff. What's the error?",
        "Can you help me debug this Python server issue?",
        "helpful"
    )
    
    # Test memory search
    technical_memories = conversation.search_memories("server python debug", ["conversation"])
    print("Technical memories found:", len(technical_memories))
    
    # Get insights
    insights = conversation.get_memory_insights()
    print("Relationship insights:", insights['relationship_insights'])
    print("Technical insights:", insights['technical_insights'])
    
    # Test context generation
    context = conversation.get_context_for_model(include_memory=True)
    print("Generated context length:", len(context))