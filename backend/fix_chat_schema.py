from pathlib import Path

chat_path = Path(__file__).resolve().parent / "schemas" / "chat.py"
req_path = Path(__file__).resolve().parent / "requirements.txt"
chat_text = '''from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"
    use_memory: bool = True


class ChatResponse(BaseModel):
    response: str
    session_id: str
    used_memory: bool
'''
chat_path.write_text(chat_text, encoding='utf-8')
req_text = req_path.read_text(encoding='utf-8')
seen = set()
lines = []
for line in req_text.splitlines():
    if line in {"python-dotenv", "langchain", "langchain-openai", "langchain-groq"}:
        if line in seen:
            continue
        seen.add(line)
    lines.append(line)
req_path.write_text("\n".join(lines) + ("\n" if lines and lines[-1] != "" else ""), encoding='utf-8')
print('ok')
