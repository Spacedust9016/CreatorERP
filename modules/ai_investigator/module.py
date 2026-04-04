from core.module_base import ModuleBase
from core.database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from datetime import datetime
from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import os
import json
import asyncio
from config import settings


class Investigation(Base):
    __tablename__ = "investigations"
    id = Column(Integer, primary_key=True)
    query = Column(Text)
    context = Column(JSON, nullable=True)
    result = Column(Text)
    provider = Column(String(50))
    model = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)


class AIProvider(Base):
    __tablename__ = "ai_providers"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    provider_type = Column(String(20))
    api_key = Column(String(500), nullable=True)
    base_url = Column(String(500), nullable=True)
    default_model = Column(String(100))
    is_active = Column(Integer, default=1)


class InvestigationRequest(BaseModel):
    query: str
    context: Optional[Dict[str, Any]] = None
    provider: Optional[str] = None
    model: Optional[str] = None


class InvestigationResponse(BaseModel):
    result: str
    provider: str
    model: str
    query: str


class ProviderConfig(BaseModel):
    name: str
    provider_type: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    default_model: str


router = APIRouter(prefix="/api/ai", tags=["ai_investigator"])


class AIClient:
    def __init__(self):
        self.providers = {
            "local": self._call_local,
            "openai": self._call_openai,
            "anthropic": self._call_anthropic,
            "opencode": self._call_opencode,
            "custom": self._call_custom,
        }

    async def investigate(
        self,
        query: str,
        provider: str,
        model: Optional[str] = None,
        context: Optional[Dict] = None,
    ) -> Dict[str, str]:
        if provider not in self.providers:
            raise HTTPException(status_code=400, detail=f"Unknown provider: {provider}")

        handler = self.providers[provider]
        result = await handler(query, model, context)
        return result

    async def _call_local(
        self, query: str, model: Optional[str], context: Optional[Dict]
    ) -> Dict[str, str]:
        model_name = model or settings.AI_MODEL or "llama2"
        base_url = settings.AI_API_BASE or "http://localhost:11434"

        try:
            import aiohttp

            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": model_name,
                    "prompt": self._build_prompt(query, context),
                    "stream": False,
                }
                async with session.post(
                    f"{base_url}/api/generate", json=payload
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return {
                            "result": data.get("response", ""),
                            "provider": "local",
                            "model": model_name,
                        }
                    else:
                        return {
                            "result": f"Local LLM unavailable. Ensure Ollama is running at {base_url}",
                            "provider": "local",
                            "model": model_name,
                        }
        except Exception as e:
            return {
                "result": f"Local LLM error: {str(e)}. Ensure Ollama is running.",
                "provider": "local",
                "model": model_name,
            }

    async def _call_openai(
        self, query: str, model: Optional[str], context: Optional[Dict]
    ) -> Dict[str, str]:
        model_name = model or "gpt-4-turbo-preview"
        api_key = settings.OPENAI_API_KEY

        if not api_key:
            return {
                "result": "OpenAI API key not configured. Set OPENAI_API_KEY in .env",
                "provider": "openai",
                "model": model_name,
            }

        try:
            from openai import AsyncOpenAI

            client = AsyncOpenAI(api_key=api_key)
            messages = self._build_messages(query, context)
            response = await client.chat.completions.create(
                model=model_name, messages=messages, max_tokens=2000
            )
            return {
                "result": response.choices[0].message.content,
                "provider": "openai",
                "model": model_name,
            }
        except Exception as e:
            return {
                "result": f"OpenAI error: {str(e)}",
                "provider": "openai",
                "model": model_name,
            }

    async def _call_anthropic(
        self, query: str, model: Optional[str], context: Optional[Dict]
    ) -> Dict[str, str]:
        model_name = model or "claude-3-opus-20240229"
        api_key = settings.ANTHROPIC_API_KEY

        if not api_key:
            return {
                "result": "Anthropic API key not configured. Set ANTHROPIC_API_KEY in .env",
                "provider": "anthropic",
                "model": model_name,
            }

        try:
            from anthropic import AsyncAnthropic

            client = AsyncAnthropic(api_key=api_key)
            messages = self._build_anthropic_messages(query, context)
            response = await client.messages.create(
                model=model_name, max_tokens=2000, messages=messages
            )
            return {
                "result": response.content[0].text,
                "provider": "anthropic",
                "model": model_name,
            }
        except Exception as e:
            return {
                "result": f"Anthropic error: {str(e)}",
                "provider": "anthropic",
                "model": model_name,
            }

    async def _call_opencode(
        self, query: str, model: Optional[str], context: Optional[Dict]
    ) -> Dict[str, str]:
        model_name = model or "opencode-4"
        api_key = settings.OPENCODE_API_KEY
        base_url = settings.OPENCODE_API_BASE

        if not api_key:
            return {
                "result": "OpenCode API key not configured. Set OPENCODE_API_KEY in .env",
                "provider": "opencode",
                "model": model_name,
            }

        try:
            import aiohttp

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            }

            messages = self._build_messages(query, context)
            payload = {
                "model": model_name,
                "messages": messages,
                "max_tokens": 2000,
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{base_url}/chat/completions", json=payload, headers=headers
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        result = (
                            data.get("choices", [{}])[0]
                            .get("message", {})
                            .get("content", "")
                        )
                        return {
                            "result": result,
                            "provider": "opencode",
                            "model": model_name,
                        }
                    else:
                        error_text = await resp.text()
                        return {
                            "result": f"OpenCode API error: HTTP {resp.status} - {error_text}",
                            "provider": "opencode",
                            "model": model_name,
                        }
        except Exception as e:
            return {
                "result": f"OpenCode API error: {str(e)}",
                "provider": "opencode",
                "model": model_name,
            }

    async def _call_custom(
        self, query: str, model: Optional[str], context: Optional[Dict]
    ) -> Dict[str, str]:
        model_name = model or "custom-model"
        base_url = settings.AI_API_BASE
        api_key = settings.AI_API_KEY

        if not base_url:
            return {
                "result": "Custom API base URL not configured. Set AI_API_BASE in .env",
                "provider": "custom",
                "model": model_name,
            }

        try:
            import aiohttp

            headers = {"Content-Type": "application/json"}
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"

            payload = {
                "model": model_name,
                "messages": [
                    {"role": "user", "content": self._build_prompt(query, context)}
                ],
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{base_url}/chat/completions", json=payload, headers=headers
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        result = (
                            data.get("choices", [{}])[0]
                            .get("message", {})
                            .get("content", "")
                        )
                        return {
                            "result": result,
                            "provider": "custom",
                            "model": model_name,
                        }
                    else:
                        return {
                            "result": f"Custom API error: HTTP {resp.status}",
                            "provider": "custom",
                            "model": model_name,
                        }
        except Exception as e:
            return {
                "result": f"Custom API error: {str(e)}",
                "provider": "custom",
                "model": model_name,
            }

    def _build_prompt(self, query: str, context: Optional[Dict]) -> str:
        prompt = "You are a business analytics AI assistant helping content creators analyze their data.\n\n"
        if context:
            prompt += f"Context data:\n{json.dumps(context, indent=2)}\n\n"
        prompt += f"Query: {query}\n\nProvide a detailed analysis:"
        return prompt

    def _build_messages(self, query: str, context: Optional[Dict]) -> List[Dict]:
        system_msg = "You are a business analytics AI assistant helping content creators analyze their data. Provide actionable insights and recommendations."
        content = query
        if context:
            content = f"Context data:\n{json.dumps(context, indent=2)}\n\n{query}"
        return [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": content},
        ]

    def _build_anthropic_messages(
        self, query: str, context: Optional[Dict]
    ) -> List[Dict]:
        content = query
        if context:
            content = f"Context data:\n{json.dumps(context, indent=2)}\n\n{query}"
        return [{"role": "user", "content": content}]


ai_client = AIClient()


@router.post("/investigate", response_model=InvestigationResponse)
async def investigate(request: InvestigationRequest):
    provider = request.provider or settings.AI_PROVIDER or "local"
    result = await ai_client.investigate(
        query=request.query,
        provider=provider,
        model=request.model,
        context=request.context,
    )
    return InvestigationResponse(**result)


@router.get("/providers")
async def list_providers():
    return {
        "providers": [
            {
                "name": "local",
                "description": "Local LLM via Ollama",
                "config_key": "AI_API_BASE",
            },
            {
                "name": "openai",
                "description": "OpenAI GPT models",
                "config_key": "OPENAI_API_KEY",
            },
            {
                "name": "anthropic",
                "description": "Anthropic Claude models",
                "config_key": "ANTHROPIC_API_KEY",
            },
            {
                "name": "opencode",
                "description": "OpenCode AI models",
                "config_key": "OPENCODE_API_KEY",
            },
            {
                "name": "custom",
                "description": "Custom API endpoint",
                "config_keys": ["AI_API_BASE", "AI_API_KEY"],
            },
        ],
        "current_provider": settings.AI_PROVIDER,
        "current_model": settings.AI_MODEL,
    }


@router.post("/analyze/dashboard")
async def analyze_dashboard():
    from modules.social.module import SocialModule
    from modules.courses.module import CoursesModule
    from modules.finance.module import FinanceModule

    context = {
        "social": SocialModule().get_simulated_data(),
        "courses": CoursesModule().get_simulated_data(),
        "finance": FinanceModule().get_simulated_data(),
    }

    query = """Analyze my creator business dashboard and provide:
1. Key performance insights
2. Areas of strength
3. Areas needing improvement
4. Recommended actions for growth"""

    provider = settings.AI_PROVIDER or "local"
    result = await ai_client.investigate(query, provider, context=context)
    return result


@router.post("/analyze/content")
async def analyze_content():
    from modules.calendar.module import CalendarModule

    context = {"upcoming_content": CalendarModule().get_simulated_data()["upcoming"]}

    query = """Analyze my content calendar and provide:
1. Content strategy assessment
2. Platform mix optimization suggestions
3. Best posting times recommendations
4. Content ideas based on gaps"""

    provider = settings.AI_PROVIDER or "local"
    result = await ai_client.investigate(query, provider, context=context)
    return result


class AIInvestigatorModule(ModuleBase):
    name = "ai_investigator"
    version = "1.0.0"
    description = "AI-powered business intelligence and investigation"
    models = [Investigation, AIProvider]

    def register_routes(self, app):
        app.include_router(router)

    def get_simulated_data(self):
        return {
            "available_providers": [
                "local",
                "openai",
                "anthropic",
                "opencode",
                "custom",
            ],
            "default_provider": settings.AI_PROVIDER or "local",
        }
