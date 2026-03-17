# Agent Environment Configuration Templates

## Nyra VM/Container
```
agent_name: nyra
os: Windows Server 2025
ui: enabled
voice: enabled
avatar: enabled
memory_dir: /mnt/nyra_memory
api_port: 5001
permissions: [UI, voice, memory, internal_network]
```

## Copilot Container
```
agent_name: copilot
os: Windows Server Core
dev_tools: enabled
api_port: 5002
memory_dir: /mnt/copilot_memory
permissions: [codebase, memory, internal_network]
```

## G5 Orchestrator
```
agent_name: g5
os: Windows Server Core
headless: true
api_port: 5003
memory_dir: /mnt/g5_memory
permissions: [orchestration, memory, internal_network]
```

## Memory Layer Service
```
service_name: memory_layer
os: Windows Server Core
api_port: 5010
storage: /mnt/memory_storage
permissions: [read, write, backup, internal_network]
```
