# AI Client Report Generator

Расшифровка диалога → ИИ (OpenAI) → структурированный JSON → HTML-шаблон (Jinja2) → PDF (WeasyPrint) в `reports/`.

```bash
pip install -r requirements.txt
cp .env.example .env            # впишите OPENAI_API_KEY
python main.py example_dialog.txt
python main.py example_dialog.txt --design   # + изображение, сгенерированное ИИ
MOCK_AI=1 python main.py example_dialog.txt  # без API-ключа (заглушка)
```

Структура: `main.py`, `utils/ai_processor.py`, `utils/pdf_generator.py`, `utils/image_generator.py`,
`templates/report_template.html`, `reports/`. Ошибки (пустой файл, нет ключа, битый JSON, сбой API)
обрабатываются, основные этапы логируются.
