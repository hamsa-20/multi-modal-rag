import os
import json
import requests
from typing import List
from src.retriever.retriever import Retriever
from dotenv import load_dotenv

load_dotenv()

# Local model name for Ollama
LOCAL_MODEL = "llama3.1"


def build_prompt(query: str, contexts: List[dict]):
    ctx_text = ""
    for c in contexts:
        meta = c.get("meta", {})
        page = meta.get("page", "?")
        ctype = meta.get("type", "text")
        ctx_text += f"\n--- [page {page} | {ctype}] ---\n{c.get('text', '')}\n"

    return f"""
You are a helpful assistant using ONLY the provided context to answer.
If you cite a fact, include page numbers like [page X].
If the answer is not in context, say "Not found".

Context:
{ctx_text}

Question: {query}

Answer:
"""


def local_llm_call(prompt: str):
    """
    Robust streaming parser for Ollama chat API.
    Handles multiple JSON objects inside a single stream chunk.
    """
    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": LOCAL_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "stream": True
            },
            stream=True,
            timeout=120
        )

        full = ""
        buffer = ""

        for raw_chunk in response.iter_lines():
            if not raw_chunk:
                continue

            chunk = raw_chunk.decode("utf-8")

            # Append chunk to buffer
            buffer += chunk

            # Parse buffer into JSON objects
            while True:
                buffer = buffer.lstrip()
                if not buffer:
                    break

                if buffer[0] != "{":
                    # Try to recover if buffer is corrupted
                    buffer = buffer[1:]
                    continue

                brace_count = 0
                end_idx = -1

                for i, ch in enumerate(buffer):
                    if ch == "{":
                        brace_count += 1
                    elif ch == "}":
                        brace_count -= 1
                        if brace_count == 0:
                            end_idx = i
                            break

                if end_idx == -1:
                    # Not a full JSON object yet
                    break

                json_str = buffer[:end_idx + 1]
                buffer = buffer[end_idx + 1:]

                try:
                    data = json.loads(json_str)
                    if "message" in data and "content" in data["message"]:
                        full += data["message"]["content"]
                except:
                    continue

        return full.strip()

    except Exception as e:
        return f"Local LLM error: {e}"


def answer_query(query: str, retriever: Retriever, topk=5):
    """
    Main RAG pipeline function.
    Retrieves chunks, builds prompt, and runs local LLM.
    """
    hits = retriever.retrieve(query, topk=topk)

    contexts = []
    for h in hits:
        contexts.append({"meta": h["meta"], "text": h["text"]})

    prompt = build_prompt(query, contexts)

    # Pass prompt to local LLM (Ollama)
    answer = local_llm_call(prompt)
    return answer
