"""Optional: AI-generated illustration for the "design" report."""
import base64
import logging
import os
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"


def build_image_prompt(client, transcript: str) -> str:
    """Ask the text model to turn the transcript into an image-generation prompt."""
    resp = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": "По расшифровке разговора напиши ОДИН промпт на английском "
             "(до 80 слов) для генерации референса дизайна сайта клиента. Только промпт."},
            {"role": "user", "content": transcript},
        ],
    )
    return (resp.choices[0].message.content or "").strip()


def generate_design_image(transcript: str):
    """Return (image_path, prompt) or (None, None) if generation failed."""
    from openai import OpenAI, OpenAIError

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY не задан - изображение пропущено")
        return None, None
    client = OpenAI(api_key=api_key)
    model = os.getenv("OPENAI_IMAGE_MODEL", "dall-e-3")
    try:
        prompt = build_image_prompt(client, transcript)
        logger.info("Промпт для изображения (%d симв.), модель %s", len(prompt), model)
        kwargs = {"model": model, "prompt": prompt, "size": "1024x1024", "n": 1}
        if model.startswith("dall-e"):
            kwargs["response_format"] = "b64_json"
        img = client.images.generate(**kwargs)
        REPORTS_DIR.mkdir(exist_ok=True)
        path = REPORTS_DIR / f"design_{datetime.now():%Y-%m-%d_%H-%M-%S}.png"
        path.write_bytes(base64.b64decode(img.data[0].b64_json))
        logger.info("Изображение сохранено: %s", path)
        return path, prompt
    except (OpenAIError, TypeError, ValueError) as exc:
        logger.error("Не удалось сгенерировать изображение: %s", exc)
        return None, None
