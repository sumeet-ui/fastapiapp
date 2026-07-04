from pathlib import Path

base = Path(__file__).resolve().parent
chat_path = base / "schemas" / "chat.py"
req_path = base / "requirements.txt"

chat_text = """from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"
    use_memory: bool = True


class ChatResponse(BaseModel):
    response: str
    session_id: str
    used_memory: bool
"""

chat_path.write_text(chat_text, encoding="utf-8")

req_bytes = req_path.read_bytes()
for encoding in ("utf-8", "utf-16", "utf-16-le", "utf-16-be"):
    try:
        req_text = req_bytes.decode(encoding)
        break
    except UnicodeDecodeError:
        req_text = None
if req_text is None:
    req_text = req_bytes.decode("utf-8", errors="replace")

lines = []
seen = set()
for line in req_text.splitlines():
    if line in {"python-dotenv", "langchain", "langchain-openai", "langchain-groq"}:
        if line in seen:
            continue
        seen.add(line)
    lines.append(line)
req_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
print("updated")
