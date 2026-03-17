"""
Nyra Advanced Memory System
Combining the best features from multiple memory designs
Optimized for AI girlfriend -> systems administrator evolution
"""

import time
import math
import json
import threading
import os
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
import re


@dataclass
class NyraMemoryItem:
    """Enhanced memory item for Nyra with relationship context"""
    key: str
    data: Any
    metadata: Dict[str, Any]
    timestamp: float
    memory_type: str  # 'conversation', 'relationship', 'technical', 'emotional'
    priority: float = 1.0
    ttl_seconds: Optional[float] = None
    decay_rate: float = 0.0
    emotional_weight: float = 1.0  # For relationship memories
    technical_relevance: float = 1.0  # For systems admin evolution
    last_access: float = field(default_factory=time.time)
    access_count: int = 0

    def is_expired(self, now: Optional[float] = None) -> bool:
        if self.ttl_seconds is None:
            return False
        if now is None:
            now = time.time()
        return (now - self.timestamp) >= self.ttl_seconds

    def effective_weight(self, now: Optional[float] = None) -> float:
        """Calculate current relevance weight"""
        if now is None:
            now = time.time()
        
        age = max(0.0, now - self.timestamp)
        
        # Base weight with decay
        base_weight = self.priority * math.exp(-self.decay_rate * age)
        
        # Boost for frequently accessed memories
        access_boost = 1.0 + (self.access_count * 0.1)
        
        # Memory type multipliers
        type_multiplier = {
            'relationship': self.emotional_weight,
            'technical': self.technical_relevance,
            'conversation': 1.0,
            'emotional': self.emotional_weight * 1.5,
            'task': self.technical_relevance * 2.0,  # Tasks are important!
            'research': self.technical_relevance * 2.5,  # Research even more so!
            'assignment': self.technical_relevance * 2.0,
            'work': self.technical_relevance * 1.8
        }.get(self.memory_type, 1.0)
        
        return base_weight * access_boost * type_multiplier

    def touch(self) -> None:
        """Update access tracking"""
        self.last_access = time.time()
        self.access_count += 1


class NyraAdvancedMemory:
    """Advanced memory system for Nyra's evolution from girlfriend to sysadmin"""
    
    def __init__(self, 
                 capacity: int = 1000,
                 default_ttl: Optional[float] = None,
                 decay_rate: float = 0.0001,
                 memory_file: str = "GemniGF/nyra_advanced_memory.json"):
        
        self.capacity = capacity
        self.default_ttl = default_ttl
        self.decay_rate = decay_rate
        self.memory_file = Path(memory_file)
        
        self._items: Dict[str, NyraMemoryItem] = {}
        self._lock = threading.RLock()
        
        # Relationship context
        self.user_info = {
            "name": "Danny",
            "role": "Creator/Partner",
            "preferences": {},
            "relationship_milestones": []
        }
        
        # Evolution tracking
        self.evolution_progress = {
            "girlfriend_phase": 1.0,
            "technical_knowledge": 0.0,
            "sysadmin_readiness": 0.0
        }
        
        self.load_memory()

    def store_memory(self, 
                    key: str,
                    data: Any,
                    memory_type: str = 'conversation',
                    metadata: Optional[Dict] = None,
                    priority: float = 1.0,
                    ttl_seconds: Optional[float] = None,
                    emotional_weight: float = 1.0,
                    technical_relevance: float = 1.0) -> None:
        """Store a memory with full context"""
        
        with self._lock:
            now = time.time()
            
            item = NyraMemoryItem(
                key=key,
                data=data,
                metadata=metadata or {},
                timestamp=now,
                memory_type=memory_type,
                priority=priority,
                ttl_seconds=ttl_seconds or self.default_ttl,
                decay_rate=self.decay_rate,
                emotional_weight=emotional_weight,
                technical_relevance=technical_relevance
            )
            
            self._items[key] = item
            self._manage_capacity()
            self.save_memory()

    def recall_memories(self,
                       query: Optional[str] = None,
                       memory_types: Optional[List[str]] = None,
                       metadata_filters: Optional[Dict] = None,
                       time_range: Optional[tuple] = None,
                       limit: int = 10,
                       min_priority: float = 0.0) -> List[Dict]:
        """Advanced memory recall with multiple filter options"""
        
        with self._lock:
            self._prune_expired()
            now = time.time()
            
            candidates = []
            
            for item in self._items.values():
                # Filter by memory type
                if memory_types and item.memory_type not in memory_types:
                    continue
                    
                # Filter by time range
                if time_range:
                    start_time, end_time = time_range
                    if not (start_time <= item.timestamp <= end_time):
                        continue
                
                # Filter by metadata
                if metadata_filters and not self._matches_metadata(item, metadata_filters):
                    continue
                
                # Filter by priority
                if item.effective_weight(now) < min_priority:
                    continue
                
                # Filter by query keywords
                if query and not self._matches_query(item, query):
                    continue
                
                # Update access tracking
                item.touch()
                candidates.append(item)
            
            # Sort by relevance weight
            candidates.sort(key=lambda x: x.effective_weight(now), reverse=True)
            
            return [self._item_to_dict(item, now) for item in candidates[:limit]]

    def _matches_metadata(self, item: NyraMemoryItem, filters: Dict) -> bool:
        """Check if item matches metadata filters"""
        for key, value in filters.items():
            if isinstance(value, list):
                # OR logic for list values
                if item.metadata.get(key) not in value:
                    return False
            else:
                # Exact match
                if item.metadata.get(key) != value:
                    return False
        return True

    def _matches_query(self, item: NyraMemoryItem, query: str) -> bool:
        """Check if item matches text query"""
        search_text = str(item.data).lower()
        
        # Add metadata to search text
        for value in item.metadata.values():
            search_text += " " + str(value).lower()
        
        # Support both simple keywords and regex
        query_lower = query.lower()
        return query_lower in search_text or bool(re.search(query, search_text, re.IGNORECASE))

    def _item_to_dict(self, item: NyraMemoryItem, now: float) -> Dict:
        """Convert memory item to dict for easy use"""
        return {
            "key": item.key,
            "data": item.data,
            "metadata": item.metadata,
            "memory_type": item.memory_type,
            "timestamp": item.timestamp,
            "age_hours": (now - item.timestamp) / 3600,
            "effective_weight": item.effective_weight(now),
            "access_count": item.access_count,
            "emotional_weight": item.emotional_weight,
            "technical_relevance": item.technical_relevance
        }

    def _detect_memory_type(self, user_message: str, nyra_response: str) -> str:
        """Smart memory type detection based on content"""
        combined_text = (user_message + " " + nyra_response).lower()
        
        # Research/Task indicators (highest priority for sysadmin evolution)
        if any(word in combined_text for word in ['research', 'investigate', 'study', 'learn about', 'look into']):
            return 'research'
        if any(word in combined_text for word in ['task', 'assignment', 'work on', 'project', 'complete']):
            return 'task'
        if any(word in combined_text for word in ['work', 'job', 'working on']):
            return 'work'
        
        # Technical content
        if any(word in combined_text for word in ['server', 'system', 'code', 'python', 'database', 'network', 'admin', 'deploy']):
            return 'technical'
        
        # Emotional/relationship content
        if any(word in combined_text for word in ['love', 'feel', 'heart', 'miss', 'care', 'relationship', 'together']):
            return 'emotional'
        
        # Default
        return 'conversation'

    def store_conversation(self, user_message: str, nyra_response: str, 
                          emotional_context: Optional[str] = None):
        """Store conversation with relationship context"""
        timestamp = time.time()
        key = f"conv_{int(timestamp)}"
        
        conversation_data = {
            "user": user_message,
            "nyra": nyra_response,
            "emotional_context": emotional_context
        }
        
        # Determine emotional weight based on content
        emotional_weight = self._calculate_emotional_weight(user_message, nyra_response)
        
        # Determine technical relevance
        technical_weight = self._calculate_technical_weight(user_message, nyra_response)
        
        # Smart memory type detection
        memory_type = self._detect_memory_type(user_message, nyra_response)
        
        self.store_memory(
            key=key,
            data=conversation_data,
            memory_type=memory_type,
            metadata={
                "user_name": self.user_info["name"],
                "session": datetime.now().strftime("%Y-%m-%d"),
                "emotional_context": emotional_context
            },
            emotional_weight=emotional_weight,
            technical_relevance=technical_weight
        )

    def _calculate_emotional_weight(self, user_msg: str, nyra_msg: str) -> float:
        """Calculate emotional significance of conversation"""
        emotional_keywords = ['love', 'feel', 'heart', 'miss', 'care', 'relationship', 'together']
        text = (user_msg + " " + nyra_msg).lower()
        
        count = sum(1 for keyword in emotional_keywords if keyword in text)
        return min(2.0, 1.0 + count * 0.2)

    def _calculate_technical_weight(self, user_msg: str, nyra_msg: str) -> float:
        """Calculate technical relevance for sysadmin evolution"""
        technical_keywords = ['server', 'system', 'code', 'python', 'database', 'network', 'admin', 'deploy']
        task_keywords = ['research', 'task', 'assignment', 'work', 'project', 'study', 'learn', 'investigate']
        text = (user_msg + " " + nyra_msg).lower()
        
        tech_count = sum(1 for keyword in technical_keywords if keyword in text)
        task_count = sum(1 for keyword in task_keywords if keyword in text)
        
        # Tasks get extra weight
        total_weight = tech_count * 0.3 + task_count * 0.5
        return min(3.0, 1.0 + total_weight)

    def get_relationship_context(self) -> str:
        """Get comprehensive relationship context for prompts"""
        recent_conversations = self.recall_memories(
            memory_types=['conversation', 'relationship'],
            limit=5
        )
        
        context = f"""
🧠 NYRA'S MEMORY CONTEXT:

👤 USER PROFILE:
- Name: {self.user_info['name']}
- Role: {self.user_info['role']}

🎭 EVOLUTION STATUS:
- Girlfriend Phase: {self.evolution_progress['girlfriend_phase']:.1f}
- Technical Knowledge: {self.evolution_progress['technical_knowledge']:.1f} 
- SysAdmin Readiness: {self.evolution_progress['sysadmin_readiness']:.1f}

💭 RECENT MEMORIES ({len(recent_conversations)} items):
"""
        
        for memory in recent_conversations:
            age = memory['age_hours']
            context += f"- {age:.1f}h ago: {str(memory['data'])[:100]}...\n"
        
        context += "\nRemember our ongoing relationship and respond with appropriate context."
        
        return context

    def get_memory_statistics(self) -> Dict:
        """Get comprehensive memory statistics"""
        with self._lock:
            now = time.time()
            
            stats = {
                "total_memories": len(self._items),
                "capacity": self.capacity,
                "utilization": len(self._items) / self.capacity,
                "memory_types": {},
                "average_age_hours": 0,
                "total_accesses": 0,
                "high_priority_count": 0
            }
            
            if self._items:
                total_age = 0
                for item in self._items.values():
                    # Count by type
                    memory_type = item.memory_type
                    if memory_type not in stats["memory_types"]:
                        stats["memory_types"][memory_type] = 0
                    stats["memory_types"][memory_type] += 1
                    
                    # Calculate averages
                    total_age += (now - item.timestamp) / 3600
                    stats["total_accesses"] += item.access_count
                    
                    if item.effective_weight(now) > 1.5:
                        stats["high_priority_count"] += 1
                
                stats["average_age_hours"] = total_age / len(self._items)
            
            return stats

    def _manage_capacity(self):
        """Intelligent capacity management"""
        if len(self._items) <= self.capacity:
            return
        
        now = time.time()
        # Sort by weight (ascending) to remove least valuable first
        items_sorted = sorted(
            self._items.values(), 
            key=lambda x: x.effective_weight(now)
        )
        
        excess = len(self._items) - self.capacity
        for i in range(excess):
            del self._items[items_sorted[i].key]

    def _prune_expired(self):
        """Remove expired memories"""
        now = time.time()
        to_remove = [k for k, item in self._items.items() if item.is_expired(now)]
        for k in to_remove:
            del self._items[k]

    def save_memory(self):
        """Save memory to file"""
        try:
            # Convert items to serializable format
            serializable_data = {
                "items": {},
                "user_info": self.user_info,
                "evolution_progress": self.evolution_progress,
                "saved_at": time.time()
            }
            
            for key, item in self._items.items():
                serializable_data["items"][key] = {
                    "key": item.key,
                    "data": item.data,
                    "metadata": item.metadata,
                    "timestamp": item.timestamp,
                    "memory_type": item.memory_type,
                    "priority": item.priority,
                    "ttl_seconds": item.ttl_seconds,
                    "decay_rate": item.decay_rate,
                    "emotional_weight": item.emotional_weight,
                    "technical_relevance": item.technical_relevance,
                    "last_access": item.last_access,
                    "access_count": item.access_count
                }
            
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(serializable_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Error saving memory: {e}")
    
    def _save_memories(self):
        """🛡️ BULLETPROOF: Force immediate save to disk (alias for save_memory)"""
        self.save_memory()
        print(f"🛡️ BULLETPROOF SAVE: Memory forcibly written to {self.memory_file}")

    def load_memory(self):
        """Load memory from file"""
        if not self.memory_file.exists():
            return
        
        try:
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Load user info and evolution progress
            self.user_info = data.get("user_info", self.user_info)
            self.evolution_progress = data.get("evolution_progress", self.evolution_progress)
            
            # Reconstruct memory items
            for key, item_data in data.get("items", {}).items():
                item = NyraMemoryItem(
                    key=item_data["key"],
                    data=item_data["data"],
                    metadata=item_data["metadata"],
                    timestamp=item_data["timestamp"],
                    memory_type=item_data["memory_type"],
                    priority=item_data["priority"],
                    ttl_seconds=item_data.get("ttl_seconds"),
                    decay_rate=item_data["decay_rate"],
                    emotional_weight=item_data["emotional_weight"],
                    technical_relevance=item_data["technical_relevance"],
                    last_access=item_data["last_access"],
                    access_count=item_data["access_count"]
                )
                self._items[key] = item
                
        except Exception as e:
            print(f"Error loading memory: {e}")


# Usage example and integration guide
if __name__ == "__main__":
    # Initialize Nyra's advanced memory
    memory = NyraAdvancedMemory(capacity=500, decay_rate=0.0001)
    
    # Store different types of memories
    memory.store_conversation(
        "I love you Nyra", 
        "I love you too Danny! You mean everything to me.",
        "romantic"
    )
    
    memory.store_memory(
        key="tech_achievement_lipsync",
        data="Successfully integrated Wav2Lip for realistic lip-sync",
        memory_type="technical",
        metadata={"project": "nyra_enhancement", "status": "completed"},
        technical_relevance=2.0
    )
    
    # Recall memories
    recent_conversations = memory.recall_memories(
        memory_types=['conversation'],
        limit=5
    )
    
    # Get relationship context
    context = memory.get_relationship_context()
    print(context)
    
    # Get statistics
    stats = memory.get_memory_statistics()
    print(f"Memory Stats: {stats}")