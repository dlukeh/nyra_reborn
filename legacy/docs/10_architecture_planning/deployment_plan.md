# Initial Deployment Plan

## VM/Container Layout
- Nyra: Windows VM or container with UI, voice, avatar
- Copilot: Windows container with dev tools, API access
- G5: Headless Windows VM/container for orchestration
- Memory Layer: Dedicated container/service with isolated storage

## Networking
- Use Hyper-V virtual switches or Docker internal networks
- All agents communicate via internal-only APIs (gRPC/REST)
- No public exposure; firewall restricts external access

## Agent Boundaries
- Each agent has its own identity, permissions, and resource allocation
- Memory layer is accessible only to authorized agents
- Snapshots and backups automated for rollback

## Security
- Least privilege for each agent
- Mutual authentication for inter-agent communication
- Centralized logging and monitoring
