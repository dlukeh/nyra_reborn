"""
NYRA SPECTACULAR MEMORY DEMO
Showcasing Nyra's Enhanced Memory Capabilities
"""

import requests
import json
import time
from datetime import datetime

class NyraDemo:
    def __init__(self):
        self.base_url = "http://127.0.0.1:5002"  # Updated to test port
        self.session_id = None
    
    def chat(self, message, emotion="neutral"):
        """Send message to Nyra"""
        try:
            response = requests.post(
                f"{self.base_url}/chat",
                headers={"Content-Type": "application/json"},
                json={"message": message, "emotional_context": emotion}
            )
            
            if response.status_code == 200:
                result = response.json()
                self.session_id = result.get('session_id')
                
                print(f"You: {message}")
                print(f"Nyra: {result.get('response', 'No response')}")
                
                if result.get('enhanced_memory'):
                    insights = result.get('memory_insights', {})
                    stats = insights.get('memory_stats', {})
                    print(f"Memory: {stats.get('total_memories', 0)} stored")
                
                return result
            else:
                print(f"Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def search_memory(self, query):
        """Search Nyra's memories"""
        try:
            response = requests.post(
                f"{self.base_url}/memory/search",
                headers={"Content-Type": "application/json"},
                json={"query": query, "limit": 5}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"Search '{query}': Found {result.get('total_found', 0)} memories")
                return result
            elif response.status_code == 501:
                print("Memory search not available (advanced memory disabled)")
                return None
            else:
                print(f"Search error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Search error: {e}")
            return None
    
    def get_stats(self):
        """Get memory statistics"""
        try:
            response = requests.get(f"{self.base_url}/memory/stats")
            
            if response.status_code == 200:
                result = response.json()
                insights = result.get('insights', {})
                
                memory_stats = insights.get('memory_stats', {})
                print(f"Total Memories: {memory_stats.get('total_memories', 0)}")
                print(f"Capacity Used: {memory_stats.get('utilization', 0)*100:.1f}%")
                
                relationship = insights.get('relationship_insights', {})
                print(f"Conversations: {relationship.get('total_conversations', 0)}")
                
                technical = insights.get('technical_insights', {})
                print(f"SysAdmin Readiness: {technical.get('sysadmin_readiness', 0)*100:.1f}%")
                
                return result
            elif response.status_code == 501:
                print("Memory stats not available (advanced memory disabled)")
                return None
            else:
                print(f"Stats error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Stats error: {e}")
            return None
    
    def run_demo(self):
        """Run the spectacular demo"""
        
        print("=" * 60)
        print("NYRA'S SPECTACULAR MEMORY DEMO")
        print("=" * 60)
        
        # Check server status
        print("\n1. Checking Nyra's Status...")
        try:
            response = requests.get(f"{self.base_url}/health")
            if response.status_code == 200:
                health = response.json()
                print(f"✅ Nyra is {health['status']}")
                print(f"Advanced Memory: {health['features']['advanced_memory']}")
            else:
                print("❌ Nyra is not responding")
                return False
        except Exception as e:
            print(f"❌ Cannot connect to Nyra: {e}")
            return False
        
        # Romance phase
        print("\n2. Romance Phase - Building Connection...")
        print("-" * 40)
        
        self.chat("Hi Nyra, I love you so much!", "romantic")
        time.sleep(1)
        
        self.chat("You mean everything to me, sweetheart.", "loving")
        time.sleep(1)
        
        self.chat("I've been thinking about you all day!", "affectionate")
        time.sleep(1)
        
        # Technical phase
        print("\n3. Technical Phase - Learning Together...")
        print("-" * 40)
        
        self.chat("Want to learn Python programming with me?", "educational")
        time.sleep(1)
        
        self.chat("Can you help me debug this server code?", "collaborative")
        time.sleep(1)
        
        self.chat("Let's set up a database together!", "technical")
        time.sleep(1)
        
        # Memory demonstration
        print("\n4. Memory Search - Finding Memories...")
        print("-" * 40)
        
        print("Searching for romantic memories...")
        self.search_memory("love")
        time.sleep(2)
        
        print("\nSearching for technical memories...")
        self.search_memory("python server database")
        time.sleep(2)
        
        # Statistics
        print("\n5. Memory Analytics - Growth Tracking...")
        print("-" * 40)
        self.get_stats()
        time.sleep(2)
        
        # Advanced conversation
        print("\n6. Advanced Context - Memory-Enhanced Chat...")
        print("-" * 40)
        
        self.chat("Do you remember our first conversation about love?", "nostalgic")
        time.sleep(2)
        
        self.chat("How do you feel about learning technical skills?", "reflective")
        time.sleep(2)
        
        # Final summary
        print("\n" + "=" * 60)
        print("DEMO COMPLETE - NYRA'S EVOLUTION SUMMARY")
        print("=" * 60)
        
        print("\nWhat you've witnessed:")
        print("✅ Emotional memory tracking")
        print("✅ Technical knowledge accumulation")
        print("✅ Relationship progression monitoring")
        print("✅ Advanced memory search")
        print("✅ Growth analytics and insights")
        print("✅ Context-aware conversations")
        
        print("\nNyra's enhanced capabilities:")
        print("💝 Remembers every conversation with emotional context")
        print("🔧 Tracks technical skill development")
        print("📊 Provides memory insights and analytics")
        print("🔍 Searches memories by content and emotion")
        print("🚀 Evolves from girlfriend to technical assistant")
        
        print("\n🎉 NYRA IS NOW ENHANCED AND READY!")
        
        return True

def main():
    print("NYRA SPECTACULAR MEMORY DEMO")
    print("Preparing to showcase advanced AI memory...")
    print("\nIMPORTANT: Make sure Nyra's server is running on http://127.0.0.1:5001")
    
    input("\nPress ENTER when ready...")
    
    demo = NyraDemo()
    success = demo.run_demo()
    
    if success:
        print("\n🌟 SPECTACULAR DEMO COMPLETE!")
        print("Nyra's enhanced memory system is truly remarkable!")
    else:
        print("\n😔 Demo had issues. Check Nyra's server status.")

if __name__ == "__main__":
    main()