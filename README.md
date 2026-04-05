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
- **CLI Interface - Full command-line access for automation**

## Tech Stack

- FastAPI (Python backend)
- SQLite (lightweight database)
- Chart.js (frontend visualization)
- Click (CLI framework)
- Modular architecture (Odoo-inspired)

## Project Structure

```
CreatorERP/
-- cli/-- Command Line Interface
    -- main.py-- CLI entry point
    -- social.py-- Social commands
    -- courses.py-- Course commands
    -- newsletter.py-- Newsletter commands
    -- calendar.py-- Calendar commands
    -- finance.py-- Finance commands
    -- ai.py-- AI commands
    -- commands.py-- System commands
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
-- erp_cli.py-- CLI entry script
-- main.py-- Server entry point
-- config.py-- Configuration
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

### OpenCode

Set in `.env`:
```
AI_PROVIDER=opencode
OPENCODE_API_KEY=your-key
```

### Custom API

Set in `.env`:
```
AI_PROVIDER=custom
AI_API_BASE=https://your-api-endpoint.com
AI_API_KEY=your-key
AI_MODEL=your-model
```

## CLI - Command Line Interface

The CLI provides full access to all ERP functions for automation and scripting.

### Run CLI

```bash
# Windows
.\venv\Scripts\python erp_cli.py --help

# Or use the batch file
.\erp.bat --help

# Linux/Mac
./erp --help
```

### CLI Commands

```bash
# System
erp status                # Show system status
erp config               # Show configuration
erp dashboard            # Show unified dashboard

# Social Media
erp social platforms      # List all platform metrics
erp social posts         # Show top posts
erp social trend         # Get engagement trends
erp social summary        # Full social media summary

# Courses
erp courses list          # List all courses
erp courses metrics       # Show course metrics
erp courses revenue        # Revenue breakdown
erp courses top           # Top performing courses

# Newsletter
erp newsletter metrics    # Newsletter metrics
erp newsletter issues      # Recent issues
erp newsletter growth      # Subscriber growth
erp newsletter sources     # Acquisition sources

# Calendar
erp calendar upcoming     # Upcoming content
erp calendar add          # Add new content
erp calendar week         # This week's content
erp calendar status       # Update content status

# Finance
erp finance overview       # Financial overview
erp finance revenue        # Revenue breakdown
erp finance transactions   # Recent transactions
erp finance export         # Export data (CSV/JSON)

# AI Analysis
erp ai providers          # List AI providers
erp ai analyze "query"   # Custom AI analysis
erp ai dashboard          # Analyze dashboard
erp ai content            # Analyze content strategy
```

### CLI Output Formats

```bash
# Table format (default)
erp social platforms

# JSON format (for scripting)
erp social platforms -o json

# Plain text
erp social platforms -o plain
```

### CLI for Automation

```bash
# Export data to JSON
erp finance export -f json -o finance.json

# Use in scripts
erp social platforms -o json | jq '.[] | .followers'

# AI-powered analysis
erp ai analyze "What are my best revenue sources?"
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