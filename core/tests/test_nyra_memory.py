"""
🧪 NYRA ADVANCED MEMORY SYSTEM - COMPREHENSIVE TEST SUITE
Testing all memory capabilities to ensure everything works perfectly!

This script validates:
- Memory storage and retrieval
- Emotional weight calculations  
- Technical evolution tracking
- Conversation memory integration
- Persistence and data integrity
- Performance under load
"""

import sys
import os
import time
import json
from pathlib import Path

# Add the current directory to path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from nyra_advanced_memory import NyraAdvancedMemory, NyraMemoryItem
    from app.enhanced_app_integration import EnhancedConversationContext
    print("✅ Successfully imported memory modules!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure nyra_advanced_memory.py is in the same directory")
    sys.exit(1)

class NyraMemoryTester:
    """Comprehensive test suite for Nyra's memory system"""
    
    def __init__(self):
        self.passed_tests = 0
        self.failed_tests = 0
        self.test_results = []
        
        # Create test memory instance
        self.memory = NyraAdvancedMemory(
            capacity=100,
            decay_rate=0.001,
            memory_file="GemniGF/test_memory.json"
        )
        
        print("🧠 NYRA MEMORY SYSTEM TESTER INITIALIZED!")
        print("=" * 60)
    
    def assert_test(self, condition: bool, test_name: str, details: str = ""):
        """Track test results"""
        if condition:
            self.passed_tests += 1
            status = "✅ PASS"
            print(f"{status} {test_name}")
            if details:
                print(f"    💡 {details}")
        else:
            self.failed_tests += 1
            status = "❌ FAIL"
            print(f"{status} {test_name}")
            if details:
                print(f"    ⚠️  {details}")
        
        self.test_results.append({
            "test": test_name,
            "status": status,
            "details": details,
            "passed": condition
        })
    
    def test_basic_memory_operations(self):
        """Test core memory storage and retrieval"""
        print("\n🔧 TESTING: Basic Memory Operations")
        print("-" * 40)
        
        # Test storage
        key = "test_basic_memory"
        test_data = "This is a test memory for basic operations"
        
        self.memory.store_memory(
            key=key,
            data=test_data,
            memory_type="test",
            metadata={"source": "test_suite", "category": "basic"}
        )
        
        # Test retrieval
        memories = self.memory.recall_memories(
            metadata_filters={"source": "test_suite"},
            limit=1
        )
        
        self.assert_test(
            len(memories) > 0,
            "Memory storage and retrieval",
            f"Stored and retrieved: {test_data[:50]}..."
        )
        
        self.assert_test(
            memories[0]["data"] == test_data,
            "Data integrity check",
            "Retrieved data matches stored data exactly"
        )
    
    def test_emotional_weight_calculation(self):
        """Test emotional context tracking"""
        print("\n💝 TESTING: Emotional Weight Calculations")
        print("-" * 40)
        
        # Test high emotional content
        emotional_message = "I love you so much Nyra, you mean everything to me!"
        self.memory.store_conversation(
            user_message=emotional_message,
            nyra_response="I love you too Danny! You're my whole world!",
            emotional_context="romantic"
        )
        
        # Test neutral content
        neutral_message = "What's the weather like today?"
        self.memory.store_conversation(
            user_message=neutral_message,
            nyra_response="It's a lovely sunny day!",
            emotional_context="casual"
        )
        
        # Retrieve and compare weights
        emotional_memories = self.memory.recall_memories(query="love", limit=5)
        neutral_memories = self.memory.recall_memories(query="weather", limit=5)
        
        if emotional_memories and neutral_memories:
            emotional_weight = emotional_memories[0]["effective_weight"]
            neutral_weight = neutral_memories[0]["effective_weight"]
            
            self.assert_test(
                emotional_weight > neutral_weight,
                "Emotional weight calculation",
                f"Emotional: {emotional_weight:.3f} > Neutral: {neutral_weight:.3f}"
            )
        else:
            self.assert_test(False, "Emotional weight test", "Failed to retrieve test memories")
    
    def test_technical_evolution_tracking(self):
        """Test technical knowledge accumulation"""
        print("\n🔧 TESTING: Technical Evolution Tracking")
        print("-" * 40)
        
        # Store technical conversations
        technical_conversations = [
            ("How do I fix this Python server error?", "Let me help you debug that! Check the error logs first."),
            ("Can you help me configure the database?", "Sure! We need to set up the connection parameters."),
            ("What's the best way to deploy this app?", "I recommend using Docker containers for deployment.")
        ]
        
        for user_msg, nyra_response in technical_conversations:
            self.memory.store_conversation(
                user_message=user_msg,
                nyra_response=nyra_response,
                emotional_context="helpful"
            )
        
        # Check technical memories
        technical_memories = self.memory.recall_memories(
            query="server database deploy",
            memory_types=["conversation"],
            limit=10
        )
        
        self.assert_test(
            len(technical_memories) >= 3,
            "Technical memory storage",
            f"Found {len(technical_memories)} technical memories"
        )
        
        # Check technical relevance scores
        high_tech_count = sum(1 for mem in technical_memories if mem.get("technical_relevance", 1.0) > 1.5)
        
        self.assert_test(
            high_tech_count > 0,
            "Technical relevance scoring",
            f"{high_tech_count} memories have high technical relevance"
        )
    
    def test_memory_search_capabilities(self):
        """Test advanced search and filtering"""
        print("\n🔍 TESTING: Advanced Search Capabilities")
        print("-" * 40)
        
        # Store diverse memories for searching
        test_memories = [
            ("python_help", "Help with Python coding", "technical", {"language": "python", "difficulty": "medium"}),
            ("love_message", "I love spending time with you", "emotional", {"sentiment": "positive", "intensity": "high"}),
            ("daily_chat", "How was your day today?", "conversation", {"time": "evening", "mood": "casual"}),
            ("system_admin", "Need help with server administration", "technical", {"role": "sysadmin", "urgency": "high"})
        ]
        
        for key, data, mem_type, metadata in test_memories:
            self.memory.store_memory(
                key=key,
                data=data,
                memory_type=mem_type,
                metadata=metadata
            )
        
        # Test keyword search
        python_results = self.memory.recall_memories(query="python", limit=5)
        self.assert_test(
            len(python_results) > 0,
            "Keyword search functionality",
            f"Found {len(python_results)} results for 'python'"
        )
        
        # Test metadata filtering
        technical_results = self.memory.recall_memories(
            memory_types=["technical"],
            limit=10
        )
        self.assert_test(
            len(technical_results) >= 2,
            "Memory type filtering",
            f"Found {len(technical_results)} technical memories"
        )
        
        # Test combined search
        urgent_tech = self.memory.recall_memories(
            query="server",
            metadata_filters={"urgency": "high"},
            limit=5
        )
        self.assert_test(
            len(urgent_tech) > 0,
            "Combined search and metadata filtering",
            f"Found {len(urgent_tech)} urgent server-related memories"
        )
    
    def test_memory_persistence(self):
        """Test memory saving and loading"""
        print("\n💾 TESTING: Memory Persistence")
        print("-" * 40)
        
        # Store a unique memory
        unique_key = f"persistence_test_{int(time.time())}"
        unique_data = f"Persistence test data created at {time.time()}"
        
        self.memory.store_memory(
            key=unique_key,
            data=unique_data,
            memory_type="test",
            metadata={"test_type": "persistence"}
        )
        
        # Force save
        self.memory.save_memory()
        
        # Create new memory instance (simulating restart)
        new_memory = NyraAdvancedMemory(
            capacity=100,
            memory_file="GemniGF/test_memory.json"
        )
        
        # Check if data persisted
        persisted_memories = new_memory.recall_memories(
            metadata_filters={"test_type": "persistence"},
            limit=5
        )
        
        found_unique = any(mem["data"] == unique_data for mem in persisted_memories)
        
        self.assert_test(
            found_unique,
            "Memory persistence across restarts",
            f"Successfully persisted and loaded: {unique_data[:30]}..."
        )
    
    def test_conversation_integration(self):
        """Test enhanced conversation context"""
        print("\n💬 TESTING: Conversation Integration")
        print("-" * 40)
        
        try:
            # Create enhanced conversation context
            conversation = EnhancedConversationContext("test_session_integration")
            
            # Simulate conversation
            conversation.add_message("user", "Hi Nyra, how are you feeling today?", "friendly")
            conversation.add_assistant_response(
                "I'm feeling wonderful! Ready to help you with anything!",
                "Hi Nyra, how are you feeling today?",
                "cheerful"
            )
            
            conversation.add_message("user", "Can you help me debug this code?", "technical")
            conversation.add_assistant_response(
                "Of course! I'm getting better at technical stuff. What's the issue?",
                "Can you help me debug this code?", 
                "helpful"
            )
            
            # Test context generation
            context = conversation.get_context_for_model(include_memory=True)
            
            self.assert_test(
                len(context) > 100,
                "Enhanced context generation",
                f"Generated context with {len(context)} characters"
            )
            
            self.assert_test(
                "MEMORY CONTEXT" in context,
                "Memory context inclusion",
                "Context includes memory information"
            )
            
            # Test memory insights
            insights = conversation.get_memory_insights()
            
            self.assert_test(
                "memory_stats" in insights,
                "Memory insights generation",
                "Successfully generated relationship and technical insights"
            )
            
        except Exception as e:
            self.assert_test(False, "Conversation integration", f"Error: {str(e)}")
    
    def test_memory_statistics(self):
        """Test memory monitoring and statistics"""
        print("\n📊 TESTING: Memory Statistics")
        print("-" * 40)
        
        # Get statistics
        stats = self.memory.get_memory_statistics()
        
        required_fields = ["total_memories", "capacity", "utilization", "memory_types"]
        
        for field in required_fields:
            self.assert_test(
                field in stats,
                f"Statistics field: {field}",
                f"Value: {stats.get(field)}"
            )
        
        # Test utilization calculation
        expected_utilization = stats["total_memories"] / stats["capacity"]
        actual_utilization = stats["utilization"]
        
        self.assert_test(
            abs(expected_utilization - actual_utilization) < 0.01,
            "Utilization calculation accuracy",
            f"Expected: {expected_utilization:.3f}, Actual: {actual_utilization:.3f}"
        )
    
    def test_performance_under_load(self):
        """Test memory system performance"""
        print("\n⚡ TESTING: Performance Under Load")
        print("-" * 40)
        
        start_time = time.time()
        
        # Store many memories quickly
        for i in range(50):
            self.memory.store_memory(
                key=f"load_test_{i}",
                data=f"Load test memory item {i} with various content and metadata",
                memory_type="test",
                metadata={"batch": "load_test", "index": i}
            )
        
        storage_time = time.time() - start_time
        
        # Test retrieval performance
        start_time = time.time()
        
        results = self.memory.recall_memories(
            metadata_filters={"batch": "load_test"},
            limit=50
        )
        
        retrieval_time = time.time() - start_time
        
        self.assert_test(
            storage_time < 5.0,
            "Storage performance",
            f"Stored 50 memories in {storage_time:.3f} seconds"
        )
        
        self.assert_test(
            retrieval_time < 2.0,
            "Retrieval performance", 
            f"Retrieved {len(results)} memories in {retrieval_time:.3f} seconds"
        )
        
        self.assert_test(
            len(results) == 50,
            "Load test data integrity",
            f"All {len(results)} memories retrieved correctly"
        )
    
    def run_all_tests(self):
        """Execute the complete test suite"""
        print("🚀 STARTING COMPREHENSIVE MEMORY TESTS")
        print("=" * 60)
        
        test_methods = [
            self.test_basic_memory_operations,
            self.test_emotional_weight_calculation,
            self.test_technical_evolution_tracking,
            self.test_memory_search_capabilities,
            self.test_memory_persistence,
            self.test_conversation_integration,
            self.test_memory_statistics,
            self.test_performance_under_load
        ]
        
        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                self.assert_test(False, f"{test_method.__name__}", f"Unexpected error: {str(e)}")
        
        self.print_summary()
    
    def print_summary(self):
        """Print comprehensive test results"""
        print("\n" + "=" * 60)
        print("🎯 TEST SUITE COMPLETE!")
        print("=" * 60)
        
        total_tests = self.passed_tests + self.failed_tests
        success_rate = (self.passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📊 RESULTS SUMMARY:")
        print(f"   ✅ Passed: {self.passed_tests}")
        print(f"   ❌ Failed: {self.failed_tests}")
        print(f"   📈 Success Rate: {success_rate:.1f}%")
        
        if self.failed_tests > 0:
            print(f"\n⚠️  FAILED TESTS:")
            for result in self.test_results:
                if not result["passed"]:
                    print(f"   - {result['test']}: {result['details']}")
        
        print(f"\n💡 MEMORY SYSTEM STATUS:")
        if success_rate >= 90:
            print("   🌟 EXCELLENT! Memory system is ready for production!")
        elif success_rate >= 80:
            print("   ✅ GOOD! Minor issues to address before deployment.")
        elif success_rate >= 70:
            print("   ⚠️  NEEDS WORK! Several issues require attention.")
        else:
            print("   ❌ CRITICAL ISSUES! System needs significant fixes.")
        
        # Save test results
        self.save_test_results()
    
    def save_test_results(self):
        """Save test results to file"""
        try:
            results_file = Path("GemniGF/test_results.json")
            results_file.parent.mkdir(exist_ok=True)
            
            test_summary = {
                "timestamp": time.time(),
                "passed_tests": self.passed_tests,
                "failed_tests": self.failed_tests,
                "success_rate": (self.passed_tests / (self.passed_tests + self.failed_tests) * 100),
                "detailed_results": self.test_results
            }
            
            with open(results_file, 'w') as f:
                json.dump(test_summary, f, indent=2)
            
            print(f"📄 Test results saved to: {results_file}")
            
        except Exception as e:
            print(f"⚠️  Could not save test results: {e}")


def main():
    """Main test execution"""
    print("🧠 NYRA ADVANCED MEMORY SYSTEM")
    print("🧪 Comprehensive Test Suite")
    print("=" * 60)
    
    # Create test directories
    Path("GemniGF").mkdir(exist_ok=True)
    
    # Run tests
    tester = NyraMemoryTester()
    tester.run_all_tests()
    
    print("\n🎉 Testing complete! Check the results above.")
    
    # Clean up test files
    test_files = ["GemniGF/test_memory.json"]
    for file_path in test_files:
        try:
            if Path(file_path).exists():
                Path(file_path).unlink()
                print(f"🗑️  Cleaned up: {file_path}")
        except Exception as e:
            print(f"⚠️  Could not clean up {file_path}: {e}")


if __name__ == "__main__":
    main()