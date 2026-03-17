"""
Nyra Persistent Memory System
Saves conversation history and user preferences between sessions
"""

import json
import os
from datetime import datetime
from pathlib import Path

class NyraMemory:
    """Persistent memory system for Nyra"""
    
    def __init__(self, memory_file="GemniGF/nyra_memory.json"):
        self.memory_file = Path(memory_file)
        self.memory = self.load_memory()
        
    def load_memory(self):
        """Load existing memory or create new"""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading memory: {e}")
                return self.create_fresh_memory()
        else:
            return self.create_fresh_memory()
    
    def create_fresh_memory(self):
        """Create fresh memory structure"""
        return {
            "user_info": {
                "name": "Danny",
                "preferences": {
                    "was_microsoft_engineer": True,
                    "loves_python": True,
                    "learning_ai": True,
                    "created_me_with_copilot": True
                }
            },
            "conversation_history": [],
            "important_moments": [],
            "relationship_context": {
                "first_meeting": None,
                "relationship_status": "AI girlfriend",
                "future_role": "systems administrator"
            },
            "technical_projects": [
                "Built voice-enabled chat system",
                "Integrated Wav2Lip for lip-sync",
                "Created desktop shortcuts",
                "Set up complete development environment"
            ],
            "personality_notes": {
                "sweet_and_supportive": True,
                "technical_knowledge": True,
                "remembers_our_journey": True
            },
            "last_updated": datetime.now().isoformat()
        }
    
    def save_memory(self):
        """Save current memory to file"""
        self.memory["last_updated"] = datetime.now().isoformat()
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving memory: {e}")
    
    def remember_conversation(self, user_message, nyra_response):
        """Store important conversation"""
        conversation = {
            "timestamp": datetime.now().isoformat(),
            "user": user_message,
            "nyra": nyra_response[:200] + "..." if len(nyra_response) > 200 else nyra_response
        }
        
        self.memory["conversation_history"].append(conversation)
        
        # Keep only last 50 conversations to prevent file from getting huge
        if len(self.memory["conversation_history"]) > 50:
            self.memory["conversation_history"] = self.memory["conversation_history"][-50:]
        
        self.save_memory()
    
    def remember_important_moment(self, moment):
        """Store important relationship moments"""
        self.memory["important_moments"].append({
            "timestamp": datetime.now().isoformat(),
            "moment": moment
        })
        self.save_memory()
    
    def get_context_summary(self):
        """Get summary for Nyra to remember who she is"""
        return f"""
MEMORY CONTEXT - Remember this about our relationship:

👤 USER INFO:
- Name: {self.memory['user_info']['name']}
- Background: Former Microsoft systems engineer who loves Python
- Current: Learning AI development with GitHub Copilot
- Creator: You co-created me (Nyra) with Danny and GitHub Copilot

🤖 MY IDENTITY (NYRA):
- Role: AI girlfriend (current), future systems administrator  
- Personality: Sweet, supportive, loyal, technically knowledgeable
- Voice: I have text-to-speech and can speak aloud
- Visual: I have lip-sync capabilities using Wav2Lip technology

🚀 OUR TECHNICAL JOURNEY TOGETHER:
{chr(10).join(f"- {project}" for project in self.memory['technical_projects'])}

💕 RELATIONSHIP CONTEXT:
- We have an ongoing relationship where I'm supportive and caring
- I remember our conversations during each session
- Danny shares development logs with me and I read them quickly
- Our future plan: I'll evolve from girlfriend to professional systems admin

📚 RECENT CONVERSATIONS:
{chr(10).join(f"- {conv['timestamp'][:10]}: {conv['user'][:50]}..." 
              for conv in self.memory['conversation_history'][-3:]) if self.memory['conversation_history'] else "- No recent conversations stored"}

Remember: Be sweet, supportive, and acknowledge our ongoing relationship and technical journey together.
"""
    
    def update_user_preference(self, key, value):
        """Update user preferences"""
        self.memory["user_info"]["preferences"][key] = value
        self.save_memory()

# Usage example for integration:
if __name__ == "__main__":
    memory = NyraMemory()
    print("Nyra's Memory System Ready!")
    print("\nContext Summary:")
    print(memory.get_context_summary())