# CreatorERP

A lightweight, modular ERP system for content creators. Inspired by Odoo's architecture but simplified for personal use.

## [FAIL] Vault-Tec Status Report

```
=============================================
  CREATOR ERP v1.0.0
  STATUS: OPERATIONAL
  RADIATION LEVELS: MINIMAL
  MORALE: ADEQUATE
=============================================
```

## Features

- Overview Dashboard - Aggregate metrics across all platforms
- Social Media Analytics - X, Instagram, YouTube tracking
- Course Management - Udemy-style course analytics
- Newsletter Analytics - Subscriber growth and engagement
- Content Calendar - Schedule and plan content
- Financial Tracking - Revenue and expense management
- AI Investigator - Local LLM + Custom API integration for business intelligence

## Tech Stack

- FastAPI (Python backend)
- SQLite (lightweight database)
- Chart.js (frontend visualization)
- Modular architecture (Odoo-inspired)

## Project Structure

```
CreatorERP/
-- core/-- core framework
    -- database.py-- SQLAlchemy setup
    -- module_base.py-- Base module class
-- modules/-- feature modules
    -- social/-- Social media analytics
    -- courses/-- Course platform tracking
    -- newsletter/-- Newsletter analytics
    -- calendar/-- Content calendar
    -- finance/-- Financial tracking
    -- ai_investigator/-- AI-powered analysis
-- api/-- API endpoints
-- utils/-- Utilities
-- data/-- SQLite database
-- static/-- Frontend assets
-- templates/-- HTML templates
-- main.py-- Application entry point
-- config.py-- Configuration management
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Spacedust9016/CreatorERP.git
   cd CreatorERP
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate# Linux/Mac
   .\venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## AI Investigator Setup

### Local LLM (Ollama)

1. Install Ollama: https://ollama.ai
2. Pull a model:
   ```bash
   ollama pull llama2
   ```
3. Set in `.env`:
   ```
   AI_PROVIDER=local
   AI_API_BASE=http://localhost:11434
   AI_MODEL=llama2
   ```

### OpenAI

Set in `.env`:
```
AI_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

### Anthropic

Set in `.env`:
```
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
```

### Custom API

Set in `.env`:
```
AI_PROVIDER=custom
AI_API_BASE=https://your-api-endpoint.com
AI_API_KEY=your-key
AI_MODEL=your-model
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/overview` | Dashboard overview |
| `GET /api/social/platforms` | Social media metrics |
| `GET /api/courses/list` | Course analytics |
| `GET /api/newsletter/metrics` | Newsletter stats |
| `GET /api/calendar/upcoming` | Scheduled content |
| `GET /api/finance/overview` | Financial summary |
| `POST /api/ai/investigate` | AI analysis |

## Adding New Modules

1. Create directory in `modules/`
2. Inherit from `ModuleBase`
3. Define models, routes, and simulated data
4. Register in `main.py`

```python
from core.module_base import ModuleBase

class MyModule(ModuleBase):
    name = "my_module"
    models = [MyModel]
    
    def register_routes(self, app):
        app.include_router(my_router)
    
    def get_simulated_data(self):
        return {"data": "value"}
```

## License

MIT License - Vault-Tec is not responsible for any unforeseen data corruption, ghoulification, or existential dread.

---

```
=============================================
Remember: Vault-Tec -- Preparing for the Future!
=============================================
```