"""HTML template + data -> PDF."""
import logging
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "templates"
REPORTS_DIR = ROOT / "reports"


def render_html(data: dict, template_name: str = "report_template.html") -> str:
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR),
                      autoescape=select_autoescape(["html"]))
    context = {**data, "image_path": data.get("image_path", ""), "generation_date": datetime.now().strftime("%d.%m.%Y %H:%M")}
    logger.info("Подстановка данных в шаблон %s", template_name)
    return env.get_template(template_name).render(**context)


def generate_pdf(data: dict, template_name: str = "report_template.html") -> Path:  # noqa: E501
    """Render the template and save report_YYYY-MM-DD_HH-MM-SS.pdf into reports/."""
    from weasyprint import HTML  # imported lazily: needs system libs (pango)

    html = render_html(data, template_name)
    REPORTS_DIR.mkdir(exist_ok=True)
    path = REPORTS_DIR / f"report_{datetime.now():%Y-%m-%d_%H-%M-%S}.pdf"
    HTML(string=html, base_url=str(ROOT) + "/").write_pdf(path)
    logger.info("PDF сохранён: %s", path)
    return path
