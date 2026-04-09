from openai import OpenAI
import os
import logging
import json
from typing import List, Dict

from app.config import settings


logger = logging.getLogger("sentinel_scan.ai")


# =========================
# OpenAI client
# =========================

client = OpenAI(

    api_key=settings.OPENAI_API_KEY

)


# =========================
# AI Fix Generator
# =========================

def ai_fix(

    vulnerabilities: List[Dict]

) -> List[Dict]:

    if not vulnerabilities:

        logger.info("No vulnerabilities sent to AI")

        return []


    # limit payload size for stability
    vulnerabilities = vulnerabilities[:50]


    prompt = f"""
You are a senior cybersecurity engineer.

Task:
Fix the security vulnerabilities listed below.

Requirements:

• OWASP compliant fixes
• minimal code changes
• preserve original functionality
• production ready fixes
• explain why fix is secure

Return ONLY JSON list format:

[
  {{
    "file": "file path",
    "issue": "short issue",
    "severity": "low | medium | high",
    "fix": "fixed secure code",
    "explanation": "why this fix is secure"
  }}
]

Vulnerabilities JSON:
{json.dumps(vulnerabilities, indent=2)}
"""


    try:

        response = client.chat.completions.create(

            model="gpt-4o-mini",

            temperature=0.1,

            max_tokens=1500,

            messages=[

                {

                    "role": "system",

                    "content": "You are an expert secure software engineer."

                },

                {

                    "role": "user",

                    "content": prompt

                }

            ]

        )


        content = response.choices[0].message.content


        # =====================
        # safe JSON parse
        # =====================

        try:

            fixes = json.loads(content)

        except json.JSONDecodeError:

            logger.warning("AI returned invalid JSON")

            fixes = [

                {

                    "issue": "invalid_ai_output",

                    "raw_response": content

                }

            ]


        logger.info(

            f"AI generated fixes: {len(fixes)}"

        )


        return fixes


    except Exception as e:

        logger.error(

            f"AI fix error: {str(e)}"

        )

        return [

            {

                "issue": "ai_service_failed",

                "error": str(e)

            }

        ]