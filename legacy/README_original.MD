# Nyra AI Agent Demo

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
   
# GemniGF AI Agent Workspace

## Project Overview
GemniGF is a modular AI agent system built with Python, Flask, and advanced memory management. It supports persistent, trustworthy memory, agent modularity, and web-based interaction.

## Directory Structure
```
GemniGF/
├── app/                # Main application logic (Flask, integrations)
├── agents/             # AI agent modules
├── memory/             # Memory management, JSON files, utilities
├── static/             # CSS, JS, audio, images, other static assets
├── templates/          # HTML templates and components
├── tests/              # Unit/integration/system test scripts
├── data/               # Logs, analytics, uploads, persistent data
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
├── .env                # Environment variables
└── ...                 # Other essentials
```

## Setup Instructions
1. **Clone the repository**
2. **Create and activate a Python virtual environment**
  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  ```
3. **Install dependencies**
  ```powershell
  pip install -r requirements.txt
  ```
4. **Configure environment variables**
  - Copy `.env.example` to `.env` and update keys as needed.
5. **Run the application**
  ```powershell
  python app/app_web.py
  ```

## Key Features
- Modular app logic and agent design
- Persistent STM/WM/LTM memory system
- Organized static assets and templates
- Comprehensive test suite
- Data folder for logs and analytics

## Best Practices
- Keep root directory minimal (only essentials)
- Use folders for modularity and maintainability
- Update import paths after moving files
- Store secrets in `.env`, never in code
- Run tests regularly to ensure reliability

## Contributing
- Fork the repo and create a feature branch
- Follow the directory and code organization
- Submit pull requests with clear descriptions

## License
MIT

---
For questions or support, contact the project maintainer.

2. Create a `.env` file in the project folder with:
   ```
   OPENAI_API_KEY=your_openai_key
   AI_AGENT_HOST=0.0.0.0
   AI_AGENT_PORT=5000
   AI_AGENT_DEBUG=0
   ```

## Running

- Start the server:
  ```
  python server.py
  ```
- Start the client (in a separate terminal):
  ```
  python client.py
  ```

## Notes


If you need to reset your Python environment:
  1. Delete or rename the existing `venv` folder (e.g., to `venvOLD`).
  2. Run `python -m venv venv` to create a new virtual environment.
  3. Activate the new environment and reinstall dependencies with `pip install -r requirements.txt`.
Test statement: File modification and save in VS Code successful.