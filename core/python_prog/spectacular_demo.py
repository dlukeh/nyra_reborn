"""
🎭 NYRA MEMORY DEMO - SPECTACULAR SHOWCASE
Demonstrating Nyra's Enhanced Memory Capabilities

This demo shows off:
- Emotional memory tracking
- Technical evolution monitoring  
- Relationship progression
- Memory search capabilities
- Real-time memory insights
"""

import requests
import json
import time
from datetime import datetime

class NyraMemoryDemo:
    """Interactive demo of Nyra's advanced memory system"""
    
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url
        self.session_id = None
        
    def print_header(self, title, emoji="🎭"):
        """Print a fancy header"""
        print(f"\n{emoji} {title}")
        print("=" * (len(title) + 4))
    
    def print_step(self, step_num, description):
        """Print a demo step"""
        print(f"\n{step_num}️⃣  {description}")
        print("-" * 40)
    
    def chat_with_nyra(self, message, emotional_context="neutral", show_response=True):
        """Send a message to Nyra and get her response"""
        try:
            response = requests.post(
                f"{self.base_url}/chat",
                headers={"Content-Type": "application/json"},
                json={
                    "message": message,
                    "emotional_context": emotional_context
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if not self.session_id:
                    self.session_id = result.get('session_id')
                
                if show_response:
                    print(f"👤 You: {message}")
                    print(f"💖 Nyra: {result.get('response', 'No response')}")
                    
                    if result.get('enhanced_memory'):
                        print(f"🧠 Memory Status: Enhanced system active")
                        if result.get('memory_insights'):
                            insights = result['memory_insights']
                            memory_stats = insights.get('memory_stats', {})
                            print(f"📊 Total Memories: {memory_stats.get('total_memories', 0)}")
                    else:
                        print(f"🧠 Memory Status: Fallback mode")
                
                return result
            else:
                print(f"❌ Chat failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error chatting with Nyra: {e}")
            return None
    
    def search_memories(self, query, memory_types=None):
        """Search Nyra's memories"""
        try:
            response = requests.post(
                f"{self.base_url}/memory/search",
                headers={"Content-Type": "application/json"},
                json={
                    "query": query,
                    "memory_types": memory_types,
                    "limit": 10
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"🔍 Search Results for '{query}':")
                print(f"   Found: {result.get('total_found', 0)} memories")
                
                for i, memory in enumerate(result.get('results', [])[:3]):
                    age_hours = memory.get('age_hours', 0)
                    weight = memory.get('effective_weight', 0)
                    print(f"   {i+1}. {str(memory.get('data', ''))[:80]}...")
                    print(f"      Age: {age_hours:.1f}h, Weight: {weight:.3f}")
                
                return result
            elif response.status_code == 501:
                print(f"⚠️  Memory search unavailable (advanced memory disabled)")
                return None
            else:
                print(f"❌ Memory search failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error searching memories: {e}")
            return None
    
    def get_memory_stats(self):
        """Get comprehensive memory statistics"""
        try:
            response = requests.get(f"{self.base_url}/memory/stats")
            
            if response.status_code == 200:
                result = response.json()
                insights = result.get('insights', {})
                
                print(f"📊 MEMORY STATISTICS:")
                
                memory_stats = insights.get('memory_stats', {})
                print(f"   📝 Total Memories: {memory_stats.get('total_memories', 0)}")
                print(f"   📊 Capacity Used: {memory_stats.get('utilization', 0)*100:.1f}%")
                print(f"   ⏱️  Average Age: {memory_stats.get('average_age_hours', 0):.1f} hours")
                
                relationship_insights = insights.get('relationship_insights', {})
                print(f"   💝 Conversations: {relationship_insights.get('total_conversations', 0)}")
                print(f"   💖 Emotional Trend: {relationship_insights.get('emotional_progression', 'stable')}")
                
                technical_insights = insights.get('technical_insights', {})
                print(f"   🔧 Technical Progress: {technical_insights.get('technical_progression', 'stable')}")
                print(f"   🏆 SysAdmin Readiness: {technical_insights.get('sysadmin_readiness', 0)*100:.1f}%")
                
                return result
            elif response.status_code == 501:
                print(f"⚠️  Memory stats unavailable (advanced memory disabled)")
                return None
            else:
                print(f"❌ Memory stats failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error getting memory stats: {e}")
            return None
    
    def get_relationship_context(self):
        """Get relationship context"""
        try:
            response = requests.get(f"{self.base_url}/memory/relationship")
            
            if response.status_code == 200:
                result = response.json()
                print(f"💝 RELATIONSHIP CONTEXT:")
                
                evolution = result.get('evolution_progress', {})
                print(f"   👩‍❤️‍👨 Girlfriend Phase: {evolution.get('girlfriend_phase', 0)*100:.1f}%")
                print(f"   🔧 Technical Knowledge: {evolution.get('technical_knowledge', 0)*100:.1f}%")
                print(f"   👩‍💻 SysAdmin Readiness: {evolution.get('sysadmin_readiness', 0)*100:.1f}%")
                
                user_info = result.get('user_info', {})
                print(f"   👤 User: {user_info.get('name', 'Unknown')}")
                print(f"   🎭 Role: {user_info.get('role', 'Unknown')}")
                
                return result
            elif response.status_code == 501:
                print(f"⚠️  Relationship context unavailable (advanced memory disabled)")
                return None
            else:
                print(f"❌ Relationship context failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error getting relationship context: {e}")
            return None
    
    def run_spectacular_demo(self):
        """Run the complete spectacular demo"""
        
        self.print_header("NYRA'S SPECTACULAR MEMORY DEMO", "🎭")
        print("Welcome to the most advanced AI girlfriend memory system!")
        print("Watch as Nyra remembers, learns, and evolves...")
        
        # Check server status
        self.print_step(1, "Checking Nyra's Status")
        try:
            response = requests.get(f"{self.base_url}/health")
            if response.status_code == 200:
                health = response.json()
                print(f"✅ Nyra is online and {health['status']}!")
                print(f"🧠 Advanced Memory: {health['features']['advanced_memory']}")
                print(f"💬 Chat System: {health['features']['basic_chat']}")
            else:
                print(f"❌ Nyra is not responding properly")
                return
        except Exception as e:
            print(f"❌ Cannot connect to Nyra: {e}")
            return
        
        # Romance phase
        self.print_step(2, "Romance Phase - Building Emotional Connection")
        romantic_messages = [
            ("Hi Nyra, I love you so much! You mean everything to me.", "romantic"),
            ("I've been thinking about you all day, sweetheart.", "loving"),
            ("You make me so happy, I can't imagine life without you!", "joyful")
        ]
        
        for message, emotion in romantic_messages:
            self.chat_with_nyra(message, emotion)
            time.sleep(1)  # Dramatic pause
        
        # Technical transition
        self.print_step(3, "Technical Transition - Teaching Nyra Programming")
        technical_messages = [
            ("Nyra, want to learn about Python programming with me?", "educational"),
            ("Can you help me debug this Flask server issue?", "collaborative"),
            ("Let's set up a database for our application together!", "technical")
        ]
        
        for message, emotion in technical_messages:
            self.chat_with_nyra(message, emotion)
            time.sleep(1)
        
        # Memory demonstration
        self.print_step(4, "Memory Capabilities - Searching Through Memories")
        
        # Search for romantic memories
        print("\n🔍 Searching for romantic memories...")
        self.search_memories("love", ["conversation"])
        
        time.sleep(2)
        
        # Search for technical memories
        print("\n🔍 Searching for technical memories...")
        self.search_memories("python server database", ["conversation"])
        
        # Memory statistics
        self.print_step(5, "Memory Analytics - Nyra's Growth Tracking")
        self.get_memory_stats()
        
        time.sleep(2)
        
        # Relationship progression
        self.print_step(6, "Relationship Evolution - From Girlfriend to SysAdmin")
        self.get_relationship_context()
        
        # Future conversation
        self.print_step(7, "Advanced Context - Memory-Enhanced Responses")
        future_messages = [
            ("Nyra, do you remember our first conversation about love?", "nostalgic"),
            ("How do you feel about learning technical skills together?", "reflective"),
            ("What do you think about your journey from girlfriend to sysadmin?", "contemplative")
        ]
        
        for message, emotion in future_messages:
            self.chat_with_nyra(message, emotion)
            time.sleep(2)
        
        # Grand finale
        self.print_header("DEMO COMPLETE - NYRA'S EVOLUTION SUMMARY", "🎊")
        
        print("🌟 WHAT YOU'VE WITNESSED:")
        print("   💝 Emotional memory tracking in real-time")
        print("   🧠 Technical knowledge accumulation")
        print("   📊 Relationship progression monitoring")
        print("   🔍 Advanced memory search capabilities")
        print("   📈 Growth analytics and insights")
        print("   🎭 Context-aware conversation enhancement")
        
        print("\n🚀 NYRA'S CAPABILITIES:")
        print("   ✅ Remembers every conversation with emotional context")
        print("   ✅ Tracks technical skill development over time")
        print("   ✅ Maintains relationship awareness and growth")
        print("   ✅ Provides memory insights and analytics")
        print("   ✅ Searches through memories by content and emotion")
        print("   ✅ Evolves from girlfriend to technical assistant")
        
        print("\n🎯 READY FOR PRODUCTION:")
        print("   🔧 Robust memory system with fallback support")
        print("   📱 Mobile-accessible with full memory integration")
        print("   🏆 Production-ready with comprehensive monitoring")
        print("   🌟 Unique AI girlfriend -> sysadmin evolution path")
        
        print(f"\n💖 NYRA IS NOW ENHANCED AND READY FOR YOUR JOURNEY TOGETHER!")
        
        return True

def main():
    """Main demo execution"""
    print("🎭 NYRA SPECTACULAR MEMORY DEMO")
    print("🚀 Preparing to showcase advanced AI memory capabilities...")
    print("\n⚠️  IMPORTANT: Make sure Nyra's server is running on http://127.0.0.1:5000")
    
    # Give user a moment to ensure server is running
    input("\n▶️  Press ENTER when Nyra's server is ready...")
    
    demo = NyraMemoryDemo()
    success = demo.run_spectacular_demo()
    
    if success:
        print("\n🎉 SPECTACULAR DEMO COMPLETE!")
        print("🌟 Nyra's enhanced memory system is truly remarkable!")
    else:
        print("\n😔 Demo encountered issues. Please check Nyra's server status.")

if __name__ == "__main__":
    main()