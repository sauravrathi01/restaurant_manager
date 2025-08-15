from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
import requests
import os
from dotenv import load_dotenv
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import re
import logging
from typing import Optional
import time
import random

# Load environment variables from backend directory
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Initialize FastAPI app
app = FastAPI(
    title="AI-Powered Menu Intelligence Widget",
    description="Generate menu descriptions and upsell suggestions using AI",
    version="1.0.0"
)

# Add rate limiting exception handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI configuration (via direct HTTP to avoid client/httpx compatibility issues)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Pydantic models for request/response


class MenuItemRequest(BaseModel):
    item_name: str
    model_version: Optional[str] = "gpt-3.5-turbo"  # Default to GPT-3.5
    
    @validator('item_name')
    def validate_item_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Item name cannot be empty')
        
        # Sanitize input - remove potentially harmful characters
        sanitized = re.sub(r'[<>"\']', '', v.strip())
        
        if len(sanitized) > 100:
            raise ValueError('Item name too long (max 100 characters)')
        
        if len(sanitized) < 2:
            raise ValueError('Item name too short (min 2 characters)')
        
        return sanitized
    
    @validator('model_version')
    def validate_model_version(cls, v):
        allowed_models = ["gpt-3.5-turbo", "gpt-4"]
        if v not in allowed_models:
            raise ValueError(f'Model version must be one of: {allowed_models}')
        return v

class MenuItemResponse(BaseModel):
    description: str
    upsell_suggestion: str
    model_used: str
    success: bool = True


# Prompt Engineering - Well-structured prompt for consistent AI responses
MENU_GENERATION_PROMPT = """
You are an expert restaurant menu copywriter and sales strategist. Your task is to create compelling menu descriptions and upsell suggestions.

For the given food item, provide:

1. A BRIEF, ATTRACTIVE DESCRIPTION (maximum 30 words):
   - Highlight key ingredients, flavors, and appeal
   - Use appetizing, descriptive language
   - Focus on what makes this dish special
   - Keep it concise and mouth-watering

2. ONE UPSELL SUGGESTION:
   - Suggest a complementary drink, side, or dessert
   - Make it sound irresistible and logical
   - Use persuasive but not pushy language
   - Format as "Pair it with [item]!" or similar

IMPORTANT RULES:
- Description must be exactly 30 words or less
- Use professional, appetizing language
- Avoid generic phrases like "delicious" or "tasty"
- Be specific about flavors, textures, and ingredients
- Make the upsell suggestion relevant and appealing

Food Item: {item_name}

Respond in this exact JSON format:
{{
    "description": "Your 30-word description here",
    "upsell_suggestion": "Your upsell suggestion here"
}}
"""

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "AI-Powered Menu Intelligence Widget API", "status": "healthy"}

@app.post("/generate-item-details", response_model=MenuItemResponse)
@limiter.limit("10/minute")  # Rate limiting: 10 requests per minute
async def generate_item_details(
    request: Request,
    body: MenuItemRequest,
    request_info: str = Depends(get_remote_address),
):
    """
    Generate menu description and upsell suggestion for a food item using AI.
    
    This endpoint:
    - Validates and sanitizes input
    - Applies rate limiting
    - Uses prompt engineering for consistent AI responses
    - Handles errors gracefully
    - Returns structured JSON response
    """
    try:
        logger.info(
            (
                "Generating details for item: %s using %s"
                % (body.item_name, body.model_version)
            )
        )
        
        # Check if OpenAI API key is configured
        if not OPENAI_API_KEY:
            # Fallback to mock response for demonstration
            logger.warning("OpenAI API key not found, using mock response")
            return MenuItemResponse(
                description=(
                    "A delicious fusion of authentic Indian spices and premium "
                    "cheese on crispy crust."
                ),
                upsell_suggestion="Pair it with a refreshing Mango Lassi!",
                model_used="mock-gpt-3.5-turbo",
            )
        
        # Prepare the prompt with the item name
        formatted_prompt = MENU_GENERATION_PROMPT.format(item_name=body.item_name)
        
        # Call OpenAI API
        # Call OpenAI Chat Completions API via HTTP (v1) with fallback if model unavailable
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        base_payload = {
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a professional restaurant menu copywriter. "
                        "Respond only with valid JSON."
                    ),
                },
                {"role": "user", "content": formatted_prompt},
            ],
            "max_tokens": 200,
            "temperature": 0.7,
        }

        model_used = body.model_version
        for _ in range(2):
            payload = dict(base_payload)
            payload["model"] = model_used
            try:
                http_response = requests.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=30,
                )
                http_response.raise_for_status()
                data = http_response.json()
                ai_response = (
                    data["choices"][0]["message"]["content"].strip()
                )
                break
            except requests.exceptions.HTTPError as e:
                # Handle model unavailability
                if (
                    e.response is not None
                    and e.response.status_code == 404
                    and model_used == "gpt-4"
                ):
                    logger.warning(
                        "Model gpt-4 unavailable; retrying with gpt-3.5-turbo"
                    )
                    model_used = "gpt-3.5-turbo"
                    continue
                # Handle rate limiting with retries and backoff
                if e.response is not None and e.response.status_code == 429:
                    logger.warning("OpenAI rate limited; backing off and retrying")
                    time.sleep(0.5 + random.uniform(0, 0.25))
                    try:
                        http_response = requests.post(
                            "https://api.openai.com/v1/chat/completions",
                            headers=headers,
                            json=payload,
                            timeout=30,
                        )
                        http_response.raise_for_status()
                        data = http_response.json()
                        ai_response = (
                            data["choices"][0]["message"]["content"].strip()
                        )
                        break
                    except Exception:
                        logger.error("OpenAI rate limit exceeded")
                        fallback_description = (
                            f"{body.item_name}: Crafted with fresh ingredients and balanced "
                            f"spices, highlighting inviting textures and aromatic flavor. "
                            f"Perfect for quick cravings and sharing."
                        )
                        return MenuItemResponse(
                            description=fallback_description,
                            upsell_suggestion="Pair it with a refreshing Mango Lassi!",
                            model_used=f"{model_used} (rate-limit-fallback)",
                        )
                # Other HTTP errors -> graceful fallback
                logger.error("OpenAI API error: %s", e)
                fallback_description = (
                    f"{body.item_name}: Crafted with fresh ingredients and balanced "
                    f"spices, delivering inviting textures and satisfying flavor."
                )
                return MenuItemResponse(
                    description=fallback_description,
                    upsell_suggestion="Pair it with a refreshing Mango Lassi!",
                    model_used=f"{model_used} (api-fallback)",
                )
            except requests.exceptions.RequestException as e:
                logger.error("OpenAI request failed: %s", e)
                fallback_description = (
                    f"{body.item_name}: Crafted with fresh ingredients and balanced "
                    f"spices, delivering inviting textures and satisfying flavor."
                )
                return MenuItemResponse(
                    description=fallback_description,
                    upsell_suggestion="Pair it with a refreshing Mango Lassi!",
                    model_used=f"{model_used} (network-fallback)",
                )
        
        # Try to parse JSON response
        try:
            import json
            parsed_response = json.loads(ai_response)
            
            # Validate the parsed response
            if not isinstance(parsed_response, dict):
                raise ValueError("Response is not a dictionary")
            
            if "description" not in parsed_response or "upsell_suggestion" not in parsed_response:
                raise ValueError("Missing required fields in response")
            
            # Additional validation for description length
            description = parsed_response["description"]
            if len(description.split()) > 30:
                logger.warning(
                    "Description too long (%d words), truncating",
                    len(description.split()),
                )
                words = description.split()[:30]
                description = " ".join(words)
            
            return MenuItemResponse(
                description=description,
                upsell_suggestion=parsed_response["upsell_suggestion"],
                model_used=model_used,
            )
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse AI response: {e}")
            # Fallback response
            return MenuItemResponse(
                description=(
                    "A delicious dish prepared with fresh ingredients and "
                    "authentic flavors."
                ),
                upsell_suggestion="Pair it with a refreshing beverage!",
                model_used=f"{body.model_version} (fallback)",
            )
    
    except requests.exceptions.HTTPError as e:
        # Handle rate limit specifically
        if e.response is not None and e.response.status_code == 429:
            logger.error("OpenAI rate limit exceeded")
            raise HTTPException(
                status_code=429,
                detail="AI service rate limit exceeded. Please try again later.",
            )
        logger.error(f"OpenAI API error: {e}")
        raise HTTPException(
            status_code=503,
            detail="AI service temporarily unavailable. Please try again later.",
        )
    except requests.exceptions.RequestException as e:
        logger.error(f"OpenAI request failed: {e}")
        raise HTTPException(status_code=503, detail="AI service request failed.")
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error. Please try again later.")

@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "openai_configured": bool(OPENAI_API_KEY),
        "rate_limiting": "enabled",
        "version": "1.0.0",
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
