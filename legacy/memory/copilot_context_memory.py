
"""
copilot_context_memory.py — Enhanced 3-Tier Memory System
Author: Daniel Howe + GitHub Copilot + ChatGPT-5
Date: 2025-11-04

Implements a local hierarchical memory model inspired by MemGPT:
- Short-Term Memory (STM): recent contextual notes
- Working Memory (WM): pinned facts / active goals
- Long-Term Memory (LTM): summarized or archived context

Fully compatible with existing JSON-based logs.
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

class CopilotContextMemory:
	"""
	A three-tier memory architecture supporting:
	  - STM (short-term): quick recall of latest events
	  - WM (working): persistent key-value state
	  - LTM (long-term): summarized archival memory
	"""

	def __init__(self, memory_file: str = "copilot_context_memory.json", personality_file: str = "nyra_personality.md"):
		self.memory_file = memory_file
		self.personality_file = personality_file
		self.context: Dict[str, Any] = {}
		self.personality: Dict[str, Any] = {}
		self.load()
		self.load_personality()
	# ------------------------------
	# Personality File Integration
	# ------------------------------
	def load_personality(self):
		"""Load and parse Nyra's personality file into memory."""
		if os.path.exists(self.personality_file):
			with open(self.personality_file, "r", encoding="utf-8") as f:
				content = f.read()
			self.personality = self.parse_personality_md(content)
		else:
			self.personality = {}

	def parse_personality_md(self, content: str) -> Dict[str, Any]:
		"""Simple parser for layered STM/WM/LTM blocks in Markdown."""
		import re
		blocks = re.split(r'^## ', content, flags=re.MULTILINE)
		result = {}
		for block in blocks:
			if block.strip():
				lines = block.strip().splitlines()
				header = lines[0].strip() if lines else ""
				result[header] = "\n".join(lines[1:]).strip()
		return result

	def update_personality(self, new_content: str):
		"""Overwrite personality file and reload."""
		with open(self.personality_file, "w", encoding="utf-8") as f:
			f.write(new_content)
		self.load_personality()

	def get_personality_block(self, block: str) -> str:
		"""Retrieve a specific block (STM, WM, LTM) from personality."""
		return self.personality.get(block, "")

	# ------------------------------
	# Core File Operations
	# ------------------------------
	def load(self):
		"""Load memory from disk or initialize new structure. Robust to empty/corrupt files."""
		if os.path.exists(self.memory_file):
			try:
				with open(self.memory_file, "r", encoding="utf-8") as f:
					content = f.read().strip()
					if not content:
						print(f"[WARN] Memory file '{self.memory_file}' is empty. Initializing new context.")
						raise ValueError("Empty file")
					self.context = json.loads(content)
			except Exception as e:
				print(f"[ERROR] Failed to load memory file '{self.memory_file}': {e}")
				self.context = {
					"stm": [],           # recent notes
					"wm": {},            # working memory (pinned facts)
					"ltm": [],           # long-term memory summaries
					"last_updated": None,
				}
		else:
			self.context = {
				"stm": [],           # recent notes
				"wm": {},            # working memory (pinned facts)
				"ltm": [],           # long-term memory summaries
				"last_updated": None,
			}

	def save(self):
		"""Persist memory context to disk."""
		self.context["last_updated"] = datetime.now().isoformat()
		with open(self.memory_file, "w", encoding="utf-8") as f:
			json.dump(self.context, f, indent=2)

	# ------------------------------
	# Short-Term Memory (STM)
	# ------------------------------
	def add_note(self, note: str):
		"""Add a timestamped note to STM and auto-consolidate if needed."""
		entry = {"timestamp": datetime.now().isoformat(), "note": note}
		self.context.setdefault("stm", []).append(entry)
		# Auto-age notes beyond limit
		self.consolidate_memory(limit=50)
		self.save()

	def get_history(self, n: int = 10) -> List[Dict[str, str]]:
		"""Return the last n STM entries."""
		return self.context.get("stm", [])[-n:]

	def consolidate_memory(self, limit: int = 50):
		"""
		Roll older STM entries into LTM once they exceed the limit.
		Summarizes older notes for efficient recall.
		"""
		stm = self.context.get("stm", [])
		if len(stm) > limit:
			old_entries = stm[:-limit]
			self.context["stm"] = stm[-limit:]
			summary = self.summarize(old_entries)
			self.context.setdefault("ltm", []).append({
				"timestamp": datetime.now().isoformat(),
				"summary": summary,
				"count": len(old_entries)
			})

	def summarize(self, entries: List[Dict[str, str]]) -> str:
		"""
		Very simple summarizer — concatenate and trim.
		Later, this can be replaced by an LLM summarizer or embedding model.
		"""
		joined = " ".join(e["note"] for e in entries)
		return joined[:600] + "..." if len(joined) > 600 else joined

	# ------------------------------
	# Working Memory (WM)
	# ------------------------------
	def set_item(self, key: str, value: Any):
		"""Store or update a working memory item."""
		self.context.setdefault("wm", {})[key] = value
		self.save()

	def get_item(self, key: str, default: Optional[Any] = None):
		"""Retrieve a working memory item."""
		return self.context.get("wm", {}).get(key, default)

	def pin_fact(self, key: str, value: Any):
		"""Alias for set_item() — semantic sugar for pinned facts."""
		self.set_item(key, value)

	# ------------------------------
	# Long-Term Memory (LTM)
	# ------------------------------
	def get_long_term(self, n: int = 5) -> List[Dict[str, str]]:
		"""Return the last n long-term summaries."""
		return self.context.get("ltm", [])[-n:]

	def recall(self, query: str) -> List[str]:
		"""
		Search STM and LTM for a keyword.
		Returns matching notes or summaries.
		"""
		query = query.lower()
		results = []

		# Search STM first
		for entry in self.context.get("stm", []):
			if query in entry["note"].lower():
				results.append(f"[STM] {entry['note']}")

		# Then search LTM summaries
		for entry in self.context.get("ltm", []):
			if query in entry["summary"].lower():
				results.append(f"[LTM] {entry['summary']}")

		return results

	# ------------------------------
	# Debug / Utility
	# ------------------------------
	def __repr__(self):
		return (
			f"CopilotContextMemory("
			f"STM={len(self.context.get('stm', []))}, "
			f"WM={len(self.context.get('wm', {}))}, "
			f"LTM={len(self.context.get('ltm', []))})"
		)

# Example usage & smoke test
if __name__ == "__main__":
	mem = CopilotContextMemory()

	# Personality sync test
	print("\n--- Personality Sync Test ---")
	# Optionally update personality file (uncomment to overwrite)
	# with open(mem.personality_file, "r", encoding="utf-8") as f:
	#     new_content = f.read()
	# mem.update_personality(new_content)
	mem.load_personality()
	print("STM Block:\n", mem.get_personality_block("STM: Current Session Context"))
	print("\nWM Block:\n", mem.get_personality_block("WM: Core Traits & Guidelines"))
	print("\nLTM Block:\n", mem.get_personality_block("LTM: Growth Milestones & Summaries"))

	# Add short-term notes
	mem.add_note("Started enhanced memory system session.")
	mem.add_note("Testing 3-tier architecture with STM/WM/LTM.")

	# Pin a fact
	mem.pin_fact("current_goal", "Integrate multi-agent memory layer across Copilot, ChatGPT-5, and Nyra.")

	# Simulate consolidation
	for i in range(60):
		mem.add_note(f"Auto-generated memory line {i}")

	# Search for a term
	hits = mem.recall("memory")
	print(f"\nFound {len(hits)} related memory snippets:")
	for h in hits[:5]:
		print(" •", h[:120])

	print("\nMemory state summary:", mem)
