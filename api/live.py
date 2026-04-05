import asyncio
import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from utils.data_simulator import DataSimulator

router = APIRouter(prefix="/api/live", tags=["live"])


@router.get("/snapshot")
async def get_snapshot():
    return DataSimulator.generate_live_snapshot()


@router.get("/stream")
async def stream_snapshot():
    async def event_generator():
        while True:
            payload = DataSimulator.generate_live_snapshot()
            yield f"data: {json.dumps(payload)}\n\n"
            await asyncio.sleep(3)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


def register_routes(app):
    app.include_router(router)
