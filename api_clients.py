import httpx
import asyncio
from typing import Dict
import os
from dotenv import load_dotenv

load_dotenv()

deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
gemma_api_key = os.getenv("GEMMA_API_KEY")
openrouter_api_key = os.getenv("OPENROUTER_API_KEY") 
openai_api_key = os.getenv("OPENAI_API_KEY" ) 
openai_api_key_ms= os.getenv("MAI_DS_R1_API_KEY")

async def get_gemma_soap(conversation: str) -> str:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {gemma_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "google/gemma-3-12b-it:free",
                    "messages": [
                        {
                            "role": "system",
                            "content": "Generate a detailed SOAP note from the following doctor-patient conversation. Include Subjective, Objective, Assessment, and Plan sections."
                        },
                        {
                            "role": "user",
                            "content": conversation
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1000
                },
                timeout=30.0
            )
            response.raise_for_status()
            response_json = response.json()
            if "choices" not in response_json:
                print(f"Unexpected Gemma API Response: {response_json}")
                return ""
            return response_json["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Gemma API Error: {str(e)}")
            return ""

async def get_deepseek_soap(conversation: str) -> str:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {deepseek_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "deepseek/deepseek-r1:free",
                    "messages": [
                        {
                            "role": "system",
                            "content": "Generate a detailed SOAP note from the following doctor-patient conversation. Include Subjective, Objective, Assessment, and Plan sections."
                        },
                        {
                            "role": "user",
                            "content": conversation
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1000
                },
                timeout=30.0
            )
            response.raise_for_status()
            response_json = response.json()
            if "choices" not in response_json:
                print(f"Unexpected DeepSeek API Response: {response_json}")
                return ""
            return response_json["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"DeepSeek API Error: {str(e)}")
            return ""

async def get_meta_llama_soap(conversation: str) -> str:
    """Fetch SOAP notes from Meta: Llama 3.3 70B Instruct API."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {openrouter_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "meta-llama/llama-3.3-70b-instruct:free",
                    "messages": [
                        {
                            "role": "system",
                            "content": "Generate a detailed SOAP note from the following doctor-patient conversation. Include Subjective, Objective, Assessment, and Plan sections."
                        },
                        {
                            "role": "user",
                            "content": conversation
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1000
                },
                timeout=30.0
            )
            response.raise_for_status()
            response_json = response.json()
            if "choices" not in response_json:
                print(f"Unexpected Meta Llama API Response: {response_json}")
                return ""
            return response_json["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Meta Llama API Error: {str(e)}")
            return ""

async def get_microsoft_mai_ds_soap(conversation: str) -> str:
    """Fetch SOAP notes from Microsoft MAI-DS-R1 API."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {openai_api_key_ms}",  # Use the OpenRouter API key
                    "Content-Type": "application/json",
                },
                json={
                    "model": "microsoft/mai-ds-r1:free",
                    "messages": [
                        {
                            "role": "system",
                            "content": "Generate a detailed SOAP note from the following doctor-patient conversation. Include Subjective, Objective, Assessment, and Plan sections."
                        },
                        {
                            "role": "user",
                            "content": conversation
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1000
                },
                timeout=30.0
            )
            response.raise_for_status()
            response_json = response.json()
            if "choices" not in response_json:
                print(f"Unexpected Microsoft MAI-DS-R1 API Response: {response_json}")
                return ""
            return response_json["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Microsoft MAI-DS-R1 API Error: {str(e)}")
            return ""

async def get_soap_notes(conversation: str) -> Dict[str, str]:
    tasks = [
        get_gemma_soap(conversation),
        get_deepseek_soap(conversation),
        get_meta_llama_soap(conversation),
        get_microsoft_mai_ds_soap(conversation)
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    soap_notes = {}
    api_names = ["gemma", "deepseek", "meta_llama", "microsoft_mai_ds"]
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"{api_names[i].capitalize()} API Error: {str(result)}")
        elif isinstance(result, str) and result.strip():
            soap_notes[api_names[i]] = result
    
    return soap_notes
