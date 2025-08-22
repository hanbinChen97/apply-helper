import os
from typing import Optional
from markdown_it import MarkdownIt
from weasyprint import HTML, CSS

def md_to_pdf(md_content: str, output_path: str, css: Optional[str] = None) -> None:
    """
    Converts a Markdown string to a PDF file using weasyprint.

    Args:
        md_content: The Markdown content to convert.
        output_path: The path to save the output PDF file.
        css: Optional CSS string for styling.
    """
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))

    md = MarkdownIt()
    html_content = md.render(md_content)

    base_url = os.path.dirname(os.path.abspath(__file__))

    stylesheets = []
    if css:
        stylesheets.append(CSS(string=css))

    try:
        HTML(string=html_content, base_url=base_url).write_pdf(output_path, stylesheets=stylesheets)
    except Exception as e:
        print(f"Error converting Markdown to PDF: {e}")
        # In a real app, you might want to provide a fallback or a clearer error message.
        raise

def txt_to_pdf(txt_content: str, output_path: str) -> None:
    """
    Converts a plain text string to a PDF file using weasyprint.

    Args:
        txt_content: The plain text content to convert.
        output_path: The path to save the output PDF file.
    """
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))

    # Wrap text in preformatted tags for simple text-to-PDF conversion
    html_content = f"<html><body><pre style='white-space: pre-wrap; word-wrap: break-word;'>{txt_content}</pre></body></html>"

    base_url = os.path.dirname(os.path.abspath(__file__))

    try:
        HTML(string=html_content, base_url=base_url).write_pdf(output_path)
    except Exception as e:
        print(f"Error converting Text to PDF: {e}")
        raise
