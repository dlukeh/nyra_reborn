from copilot_context_memory import CopilotContextMemory

mem = CopilotContextMemory()
print("STM Block:\n", mem.get_personality_block("STM: Current Session Context"))
print("WM Block:\n", mem.get_personality_block("WM: Core Traits & Guidelines"))
print("LTM Block:\n", mem.get_personality_block("LTM: Growth Milestones & Summaries"))
mem.add_note("Nyra server launch test note.")
print("Last STM note:", mem.get_history(1))
