# 🏗️ System Architecture

## Overview
The **IAM Backend** is a monolithic Flask application designed with a **Layered Architecture** pattern. It serves as the central nervous system for a wellness and productivity platform, orchestrating data between the User, the Database (Supabase), and external AI Services (OpenAI).

## 🧩 Architectural Patterns
- **Layered Architecture**: Separation of concerns into Routes, Controllers, Services, and Models.
- **Repository Pattern (Implicit)**: Direct Supabase calls within the Service/Model layer act as the data access layer.
- **Micro-Kernel (Plugins)**: The AI Agent system acts as a pluggable component that can "drive" the application via function calling.

---

## 🖼️ System Context Diagram (C4 Level 1)
High-level view of how the system interacts with external actors.

```mermaid
graph TD
    User[📱 Mobile/Web Client]
    
    subgraph "IAM Backend System"
        API[Flask API Gateway]
        Agent[🤖 AI Agent Engine]
    end
    
    DB[(🗄️ Supabase / PostgreSQL)]
    OpenAI[☁️ OpenAI GPT-4 API]
    
    User <-->|HTTP/JSON| API
    API <-->|SQL/PostgREST| DB
    API <-->|Internal Call| Agent
    Agent <-->|API Call| OpenAI
    
    style User fill:#f9f,stroke:#333
    style API fill:#bbf,stroke:#333
    style DB fill:#bfb,stroke:#333
    style OpenAI fill:#fbf,stroke:#333
```

---

## 📦 Container Diagram (C4 Level 2)
Detailed look at the application structure.

```mermaid
graph TB
    subgraph "Flask Application"
        direction TB
        
        Routes[📡 Routes / Blueprints]
        Controllers[🎮 Controllers]
        Services[⚙️ Services (Business Logic)]
        Models[📦 Data Models / Access]
        
        Routes --> Controllers
        Controllers --> Services
        Services --> Models
        
        subgraph "Cross-Cutting Concerns"
            Auth[🔐 JWT Auth Middleware]
            Utils[🛠️ Utilities / Helpers]
        end
    end
    
    Services --> Agent[🧠 Agent Service]
    
    click Routes "http://localhost:5000/api"
```

### Component Description

1.  **Routes (`/routes`)**: 
    - Entry points defining URL patterns.
    - Responsible for **routing** only. Delegates processing to Controllers.
    - Example: `auth_routes.py`, `mind_task_routes.py`.

2.  **Controllers (`/controllers`)**:
    - **Input Validation**: Ensures request data is correct (headers, body, params).
    - **HTTP Response**: Formats success/error JSON standard responses.
    - **Orchestration**: Calls one or more Services.
    - Example: `TaskController.create_task()`.

3.  **Services (`/services`)**:
    - **Business Logic**: The "Brain" of the application.
    - **Rules Enforcement**: e.g., "User cannot have two active tasks of the same type".
    - **Agent Integration**: Decides when to involve AI.
    - Example: `TaskService`, `AgentService`.

4.  **Data Layer (`/models` & `lib/db.py`)**:
    - **Supabase Client**: Direct interaction with the database.
    - **Schema Definitions**: Pydantic models or Python classes representing DB tables.

---

## 🗃️ Database Schema (ERD)
The system uses **PostgreSQL** (via Supabase). Below is the logical data model.

```mermaid
erDiagram
    USERS_IAM ||--o{ PROFILES : has
    USERS_IAM ||--o{ TASKS_MIND : owns
    USERS_IAM ||--o{ TASKS_BODY : owns
    USERS_IAM ||--o{ GOALS : sets
    USERS_IAM ||--o{ ACHIEVEMENTS : earns
    USERS_IAM ||--o{ CHAT_SESSIONS : participates
    
    TASK_TEMPLATES ||--|{ TASKS_MIND : instances
    TASK_TEMPLATES ||--|{ TASKS_BODY : instances
    
    CHAT_SESSIONS ||--o{ CHAT_MESSAGES : contains
    
    TASKS_MIND {
        uuid id PK
        uuid user_id FK
        uuid template_id FK
        string status "pending|completed|failed"
        jsonb params "Dynamic task params"
    }

    TASK_TEMPLATES {
        string key PK "unique identifier"
        string category "mind|body"
        int difficulty
        string reward_formula
    }
    
    BOT_RULES {
        uuid id PK
        jsonb condition "Time/Day triggers"
        jsonb action "Task creation logic"
    }

    GOALS {
        uuid id
        string metric_key
        float target_value
        date end_date
    }
```

---

## 🔄 Core Workflows

### 1. Task Creation Flow
```mermaid
sequenceDiagram
    participant Client
    participant Controller
    participant Service
    participant DB
    
    Client->>Controller: POST /api/tasks/mind
    Controller->>Controller: Validate JWT & Schema
    Controller->>Service: create_task(user_id, data)
    Service->>DB: Fetch Template (Validation)
    Service->>DB: Insert Task
    DB-->>Service: Task Record
    Service-->>Controller: Task Object
    Controller-->>Client: 201 Created (JSON)
```

### 2. AI Agent Interaction Flow
```mermaid
sequenceDiagram
    participant User
    participant ChatAPI
    participant AgentService
    participant OpenAI
    
    User->>ChatAPI: POST /chat/message "Give me a workout"
    ChatAPI->>AgentService: process_message(history)
    AgentService->>OpenAI: Completion (System Prompt + Tools)
    
    alt Needs Tool Execution
        OpenAI-->>AgentService: Tool Call: create_task(body_workout)
        AgentService->>AgentService: Execute create_task()
        AgentService->>OpenAI: Send Tool Result
        OpenAI-->>AgentService: "I've created your workout task!"
    end
    
    AgentService-->>ChatAPI: Response Message
    ChatAPI-->>User: JSON Response
```
