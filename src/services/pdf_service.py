from weasyprint import HTML
from markdown_it import MarkdownIt
from pathlib import Path
from src.core.logger import get_logger
from src.core.errors import PDFGenerationError
import typing

logger = get_logger(__name__)

def md_to_pdf(md_content: str, output_path: typing.Union[str, Path]):
    """
    Converts a markdown string to a PDF file.
    """
    logger.info(f"Converting markdown to PDF at {output_path}")
    try:
        md = MarkdownIt()
        html_content = md.render(md_content)
        HTML(string=html_content).write_pdf(output_path)
    except Exception as e:
        logger.error(f"Failed to generate PDF from markdown: {e}", exc_info=True)
        raise PDFGenerationError("Failed to convert markdown to PDF.") from e

def txt_to_pdf(txt_content: str, output_path: typing.Union[str, Path]):
    """
    Converts a plain text string to a PDF file.
    """
    logger.info(f"Converting text to PDF at {output_path}")
    try:
        # Using <pre> preserves whitespace and line breaks.
        # It's also important to escape HTML characters in the text to prevent rendering issues.
        import html
        escaped_content = html.escape(txt_content)
        html_content = f"<html><body><pre>{escaped_content}</pre></body></html>"
        HTML(string=html_content).write_pdf(output_path)
    except Exception as e:
        logger.error(f"Failed to generate PDF from text: {e}", exc_info=True)
        raise PDFGenerationError("Failed to convert text to PDF.") from e
