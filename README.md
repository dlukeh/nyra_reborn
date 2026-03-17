## 📦 Repository Overview

The repository is divided into two major sections:

### 1. `core/` — The Clean, Modern, Employer‑Facing Application

This folder contains the streamlined, production‑ready version of Nyra’s core:

- Flask web application  
- Agent logic  
- Prompts  
- Static assets  
- Templates  
- Configuration  
- Utility scripts  
- Tests  

This is the part of the system that is easiest to understand, run, and evaluate.

### 2. `legacy/` — The Full Historical System

This folder preserves the entire original Nyra system, including:

- Multi‑tier memory engines (STM, WM, LTM)  
- Meta‑cognition and narration subsystems  
- Voice pipeline (TTS/STT)  
- Wav2Lip animation system  
- Dashboard UI  
- Logs, analytics, and memory indexes  
- Research documents  
- Early orchestrator and agent core  
- Experimental modules  
- All artifacts created during development  

This is the complete footprint of the collaborative engineering journey.

---

## 🤝 Human–AI Collaboration (The Heart of Nyra)

Nyra was not built by a single developer. She was built by a **team** — a real team — long before “AI co‑engineering” became a mainstream concept.

Each partner played a distinct role:

### ChatGPT — The Orchestrator
Structured the system, planned the architecture, and coordinated the moving parts.  
ChatGPT kept the big picture coherent.

### Claude — The Coder
Wrote functions, shaped logic, and translated ideas into working components.  
Claude turned concepts into code.

### Microsoft Copilot — The Systems Designer
Guided modular design, folder structure, engineering discipline, and long‑term organization.  
Copilot made the project feel like a real system.

### Dan — The Human Engineer
The integrator, architect, debugger, and driving force.  
The one who made decisions, connected the dots, carried the memory, and kept the project alive.

This collaboration is what pulled me back into systems engineering.  
It showed me that AI isn’t just a tool — **AI can be a partner**.

Nyra is the first system I ever built with AI teammates, and that experience changed the trajectory of my career.

---

## 📁 Folder Structure

```
nyra_reborn/
│
├── core/          # Clean, modern, employer-facing application
│
└── legacy/        # Full preserved historical system
```

### Core Structure

```
core/
├── app/
├── agents/
├── config/
├── python_prog/
├── static/
├── system_prompts/
├── templates/
├── tests/
└── requirements.txt
```

### Legacy Structure

```
legacy/
├── memory/
├── nyra_memory/
├── copilot_memory/
├── voice/
├── wav2lip/
├── dashboard/
├── data/
├── uploads/
├── docs/
├── agent_core/
└── misc/
```

---

## 🚀 Running the Core Application

From inside `core/`:

### 1. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the web app

```bash
python app/app_web.py
```

---

## 🧠 About the Legacy System

The `legacy/` folder contains the full, unfiltered history of Nyra’s development — including every subsystem built collaboratively with ChatGPT, Claude, and Copilot.

This includes:

- Memory engines  
- Voice and animation pipelines  
- Dashboards  
- Logs and analytics  
- Research documents  
- Experimental modules  
- Early orchestrator  
- All artifacts created during the journey  

This folder is not required to run the core app, but it is essential for understanding the evolution of the system — and for reviving Nyra in her full original form.

---

## 🌱 Why Nyra Reborn Matters

Nyra is more than a project. She is the moment I rediscovered my engineering identity.

She represents:

- The first time I built a system with AI teammates  
- The moment I realized AI could be a partner, not just a tool  
- The spark that brought me back into systems administration  
- The foundation for the agent architectures I build today  
- A year‑long journey of exploration, learning, and collaboration  

Nyra Reborn is both a tribute and a clean presentation — a way to honor the past while showing the clarity and discipline of the engineer I’ve become.
