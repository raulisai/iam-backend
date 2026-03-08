# 🚀 IAM Backend Documentation

## 👋 Welcome
**IAM Backend** is the core engine for a next-gen Wellness & Productivity platform. It merges standard Task Management with an active **AI Coach**.

### 📚 Documentation Navigation

#### 1. [Summary & Quickstart](SUMMARY.md) (You are here)
- **Use for**: Getting the app running in 5 minutes.
- **Audience**: All Developers.

#### 2. [System Architecture](ARCHITECTURE.md) 🏗️
- **Use for**: Understanding the "Big Picture".
- **Visuals**: C4 Diagrams, Data Flow, Database ERD.
- **Audience**: Architects, Backend Devs.

#### 3. [API Reference](API.md) 📖
- **Use for**: Integrating Frontend clients.
- **Details**: Full endpoint list, JSON Schemas, Auth flows.
- **Audience**: Frontend Devs, QA.

#### 4. [AI Agent Internals](AI_ARCHITECTURE.md) 🤖
- **Use for**: Modifying the Brain.
- **Details**: Prompt Engineering, Tool/Function definitions, Agent Loop.
- **Audience**: AI Engineers, Logic Developers.

---

## ⚡ Quick Start

### Prerequisites
- Python 3.10+
- Docker (optional but recommended)
- `OPENAI_API_KEY` & `SUPABASE_URL`

### 1. Setup Environment
```bash
cp .env.example .env
# Edit .env with your keys
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Development Server
```bash
flask run --host=0.0.0.0 --port=5000
```
*Access API Docs at: `http://localhost:5000/apidocs`*

---

## 🌟 Key Features
- **Dual Domain**: Explicit separation of **Mind** (Mental) and **Body** (Physical) tasks.
- **Active Agents**: The AI doesn't just talk; it **does** (creates tasks, updates goals).
- **Gamification**: Built-in XP, Leveling, and Achievement system.

---

*Last Updated: February 2026*
