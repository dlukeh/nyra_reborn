# Multi-Agent Architecture Diagram (Text-Based)

```
+-------------------+      +-------------------+      +-------------------+
|   Nyra VM/Container|<---->|  Memory Layer     |<---->|   G5 Orchestrator |
|   (UI, Voice,     |      |  (WM/STM/LTM)     |      |   (Headless)      |
|   Avatar)         |      |                   |      |                   |
+-------------------+      +-------------------+      +-------------------+
        |                        ^                        |
        v                        |                        v
+-------------------+      +-------------------+      +-------------------+
| Copilot Container |<---->| Internal Network  |<---->|  Other Agents     |
| (Dev Tools, API)  |      | (gRPC/REST)       |      | (Future)          |
+-------------------+      +-------------------+      +-------------------+
```

- Each agent runs in its own VM or container for isolation
- Memory layer can be a dedicated service or volume
- Internal-only networking for secure communication
- Hyper-V provides snapshotting, GPU partitioning, rollback
