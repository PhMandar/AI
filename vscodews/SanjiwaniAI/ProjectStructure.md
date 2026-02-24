## High Level Architecture

SANJIWANIAI/
│
├── chatbot-ui/                  # Frontend chatbot (HTML + JS or React/Vue)
│   ├── public/
│   ├── src/
│   └── index.html
│
├── api-gateway/                 # FastAPI gateway to route requests to agents
│   ├── main.py
│   └── routers/
│
├── agents/
│   ├── patient_record/          # Manages patient history
│   │   ├── main.py
│   │   ├── models.py
│   │   └── db/
│   │
│   ├── medical_knowledge/       # RAG-powered suggestions
│   │   ├── main.py
│   │   ├── rag_engine.py
│   │   └── vector_store/
│   │
│   ├── scheduling/              # Appointments, reminders
│   │   ├── main.py
│   │   ├── calendar.py
│   │   └── whatsapp.py
│   │
│   ├── collaboration/           # Share info with other doctors
│   │   ├── main.py
│   │   └── secure_share.py
│   │
│   ├── emergency/               # Detect critical vitals
│   │   ├── main.py
│   │   └── alert.py
│   │
│   ├── hospitalization/         # Bed availability and booking
│   │   ├── main.py
│   │   └── hospital_api.py
│
├── mcp-integrations/           # External system connectors
│   ├── ehr/
│   ├── lab/
│   ├── pharmacy/
│   └── hospital/
│
├── shared/
│   ├── utils/                   # Common utilities
│   ├── schemas/                 # Pydantic models
│   └── config/
│
├── docker-compose.yml          # Multi-container setup
├── k8s-deployments/            # Kubernetes manifests
└── README.md