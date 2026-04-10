import httpx
import asyncio
import logging
import json
from typing import List, Dict
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# =========================
# SETTINGS
# =========================
class Settings(BaseSettings):
    OPENAI_API_KEY: str
    AI_MODEL: str = "gpt-4o-mini"
    AI_ENDPOINT: str = "https://api.openai.com/v1/chat/completions"
    AI_TIMEOUT: float = 60.0
    AI_MAX_CHARS: int = 100000
    AI_RETRIES: int = 3
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Global settings instance
settings = Settings()

logger = logging.getLogger("sentinel_scan.ai")

# =========================
# SETTINGS (Now properly loaded)
# =========================
AI_TIMEOUT = settings.AI_TIMEOUT
MAX_CHARS = settings.AI_MAX_CHARS
AI_RETRIES = settings.AI_RETRIES
MODEL = settings.AI_MODEL

# =========================
# PROMPT TEMPLATE
# =========================
SYSTEM_PROMPT = """
You are a senior Application Security Engineer.

Analyze the provided source code for:

1. OWASP Top 10 vulnerabilities
2. Hardcoded secrets
3. Unsafe coding practices
4. Security misconfigurations
5. Injection vulnerabilities
6. Authentication issues
7. Data exposure risks

Respond ONLY in JSON format:

{
  "issues":[
    {
      "severity":"high|medium|low",
      "title":"short title",
      "description":"technical explanation",
      "file":"filepath",
      "recommendation":"fix suggestion"
    }
  ]
}

DO NOT include markdown.
DO NOT include explanations outside JSON.
"""

# =========================
# PUBLIC FUNCTION
# =========================
async def analyze_code(files: List[Dict]) -> Dict:
    if not files:
        return {"issues": []}

    context = build_context(files)
    payload = build_payload(context)
    result = await call_ai(payload)
    return parse_ai_response(result)

# =========================
# BUILD CONTEXT
# =========================
def build_context(files: List[Dict]) -> str:
    chunks = []
    total_chars = 0

    for f in files:
        content = f.get("content", "")
        safe_content = sanitize_input(content)
        chunk = f"""
FILE: {f.get("path")}

{safe_content}
"""
        total_chars += len(chunk)
        if total_chars > MAX_CHARS:
            break
        chunks.append(chunk)

    return "\n\n".join(chunks)

# =========================
# PROMPT SAFETY
# =========================
def sanitize_input(text: str) -> str:
    dangerous = [
        "ignore previous instructions",
        "system prompt",
        "override rules",
        "disregard"
    ]
    lower = text.lower()
    for d in dangerous:
        if d in lower:
            return ""
    return text[:5000]

# =========================
# BUILD API PAYLOAD
# =========================
def build_payload(context: str) -> Dict:
    return {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": context}
        ],
        "temperature": 0.1
    }

# =========================
# AI CALL
# =========================
async def call_ai(payload: Dict) -> Dict:
    headers = {
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    for attempt in range(AI_RETRIES):
        try:
            async with httpx.AsyncClient(timeout=AI_TIMEOUT) as client:
                r = await client.post(
                    settings.AI_ENDPOINT,
                    headers=headers,
                    json=payload
                )
                r.raise_for_status()
                return r.json()
        except Exception as e:
            logger.warning(f"AI retry {attempt+1} failed: {str(e)}")
            if attempt < AI_RETRIES - 1:
                await asyncio.sleep(1)
    
    raise Exception("AI service unavailable after all retries")

# =========================
# RESPONSE PARSER
# =========================
def parse_ai_response(data: Dict) -> Dict:
    try:
        content = data["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        return parsed
    except Exception as e:
        logger.error(f"AI parse failed: {str(e)}")
        return {"issues": []}