from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from core.database import init_db
from config import settings
from api.overview import register_routes as register_overview
import os

app = FastAPI(
    title=settings.APP_NAME, version=settings.APP_VERSION, debug=settings.DEBUG
)

static_path = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")


@app.on_event("startup")
async def startup_event():
    init_db()
    from modules.social import SocialModule
    from modules.courses import CoursesModule
    from modules.newsletter import NewsletterModule
    from modules.calendar import CalendarModule
    from modules.finance import FinanceModule
    from modules.ai_investigator import AIInvestigatorModule

    modules = [
        SocialModule(),
        CoursesModule(),
        NewsletterModule(),
        CalendarModule(),
        FinanceModule(),
        AIInvestigatorModule(),
    ]

    for module in modules:
        module.init_models()
        module.register_routes(app)

    register_overview(app)


@app.get("/")
async def root():
    index_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "database": "connected"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
