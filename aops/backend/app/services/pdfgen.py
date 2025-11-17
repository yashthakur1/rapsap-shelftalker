"""
PDF generation service module.
Handles rendering HTML to PDF using pyppeteer.
"""

import os
import asyncio
import shutil
from pathlib import Path
from typing import Optional
from jinja2 import Template as Jinja2Template


class PDFGeneratorService:
    """Service for generating PDFs from HTML templates"""

    def __init__(self, output_dir: str = "./pdfs"):
        """
        Initialize PDF generator service.
        
        Args:
            output_dir: Directory to save generated PDFs
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def render_html_to_pdf(
        self, 
        html_string: str, 
        output_filename: str,
        page_size = "A4",
        margin: str = "0mm"
    ) -> str:
        """
        Render HTML string to PDF file using pyppeteer.
        
        Args:
            html_string: HTML content as string
            output_filename: Name of output PDF file
            page_size: Page size string ('A4', 'Letter', etc.) or dict with width/height (e.g., {'width': '95mm', 'height': '40mm'})
            margin: Page margin
            
        Returns:
            Path to generated PDF file
        """
        try:
            from pyppeteer import launch

            output_path = self.output_dir / output_filename

            # Try to find a local Chrome/Edge executable to avoid pyppeteer downloading Chromium
            def _find_chrome_executable() -> Optional[str]:
                # Environment variable overrides
                env_candidates = [
                    os.environ.get("CHROME_PATH"),
                    os.environ.get("CHROME_BIN"),
                    os.environ.get("CHROME_EXECUTABLE"),
                ]
                for c in env_candidates:
                    if c:
                        # If it's a path, check existence; if it's a command, which() will resolve
                        if os.path.exists(c):
                            return c
                        found = shutil.which(c)
                        if found:
                            return found

                # Common Windows install locations
                windows_paths = [
                    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
                    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                ]
                for p in windows_paths:
                    if os.path.exists(p):
                        return p

                # Fallback to PATH lookup
                for name in ("chrome", "google-chrome", "chromium", "chromium-browser", "msedge", "edge"):
                    path = shutil.which(name)
                    if path:
                        return path

                return None

            chrome_path = _find_chrome_executable()

            launch_kwargs = {"headless": True, "args": ["--no-sandbox"]}
            if chrome_path:
                launch_kwargs["executablePath"] = chrome_path
            
            # Launch browser
            browser = await launch(**launch_kwargs)
            page = await browser.newPage()
            
            # Set viewport size based on page dimensions
            # For shelf talkers and small formats, use appropriate viewport
            viewport_width = 1200
            viewport_height = 1600
            
            if isinstance(page_size, dict):
                # Parse custom dimensions to adjust viewport
                width_str = page_size.get("width", "95mm")
                height_str = page_size.get("height", "40mm")
                # For small custom sizes, use smaller viewport
                if "mm" in width_str:
                    viewport_width = int(float(width_str.replace("mm", "")) * 3.78)  # mm to px at 96 DPI
                if "mm" in height_str:
                    viewport_height = int(float(height_str.replace("mm", "")) * 3.78)
            
            await page.setViewport({"width": viewport_width, "height": viewport_height})

            # Some pyppeteer versions have different signatures for setContent; to avoid
            # compatibility issues we write the HTML into the document via evaluate.
            try:
                await page.evaluate("""
                    (html) => {
                        document.open();
                        document.write(html);
                        document.close();
                    }
                """, html_string)
            except Exception:
                # Fallback to setContent if evaluate approach fails
                await page.setContent(html_string)

            # Wait for content to be fully rendered and network to be idle
            await asyncio.sleep(2)
            
            # Prepare PDF options
            pdf_options = {
                "path": str(output_path),
                "margin": {
                    "top": margin,
                    "right": margin,
                    "bottom": margin,
                    "left": margin
                },
                "printBackground": True,
                # Prefer CSS @page size when available; otherwise width/height fallbacks are used
                "preferCSSPageSize": True
            }
            
            # Handle page_size: string preset or dict with custom dimensions
            if isinstance(page_size, dict):
                # Custom dimensions provided
                # Ensure we pass CSS-friendly strings like '95mm'
                pdf_options["width"] = page_size.get("width", "95mm")
                pdf_options["height"] = page_size.get("height", "40mm")
                # Also update viewport to match roughly the CSS size (px conversion)
                try:
                    w = str(pdf_options["width"])
                    h = str(pdf_options["height"])
                    if w.endswith('mm'):
                        viewport_width = int(float(w.replace('mm', '')) * 96.0 / 25.4)
                    if h.endswith('mm'):
                        viewport_height = int(float(h.replace('mm', '')) * 96.0 / 25.4)
                    await page.setViewport({"width": max(800, viewport_width), "height": max(600, viewport_height)})
                except Exception:
                    # ignore viewport adjustment failures
                    pass
            else:
                # Standard format string (A4, Letter, etc.)
                pdf_options["format"] = page_size
            
            # Generate PDF
            await page.pdf(pdf_options)
            
            await browser.close()
            print(f"✓ PDF generated: {output_path}")
            return str(output_path)
            
        except Exception as e:
            # Provide more actionable error message when Chromium download fails
            msg = str(e)
            if "chromium" in msg.lower() or "downloadable not found" in msg.lower() or "NoSuchKey" in msg:
                msg = (
                    "Chromium/Chrome launch failed. Ensure Chrome or Edge is installed on the host, or set the "
                    "environment variable CHROME_PATH (or CHROME_BIN / CHROME_EXECUTABLE) to the browser executable path. "
                    "Example (Windows): C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
                )
            print(f"✗ Error generating PDF: {msg}")
            raise

    def render_template(
        self, 
        template_html: str, 
        context: dict
    ) -> str:
        """
        Render Jinja2 template with context data.
        
        Args:
            template_html: HTML template string with Jinja2 syntax
            context: Dictionary of variables for template rendering
            
        Returns:
            Rendered HTML string
        """
        try:
            jinja_template = Jinja2Template(template_html)
            return jinja_template.render(context)
        except Exception as e:
            print(f"✗ Error rendering template: {e}")
            raise

    def _resolve_page_size(self, page_size) -> dict:
        """
        Normalize page size information for both PDF options and template styling.
        Returns dict with keys `pdf_size`, `css`, `label_width`, `label_height`.
        """
        default_width = "95mm"
        default_height = "40mm"
        label_width = default_width
        label_height = default_height
        if isinstance(page_size, dict):
            width = page_size.get("width")
            height = page_size.get("height")
            if width:
                label_width = width
            if height:
                label_height = height
            css_value = f"{label_width} {label_height}"
            pdf_size = {"width": label_width, "height": label_height}
        else:
            css_value = page_size or "A4"
            pdf_size = page_size or "A4"

        return {
            "pdf_size": pdf_size,
            "css": css_value,
            "label_width": label_width,
            "label_height": label_height
        }

    async def generate_batch_pdf(
        self, 
        offers: list, 
        template_html: str,
        layout_options: dict = None,
        output_filename: str = "offers_batch.pdf"
    ) -> str:
        """
        Generate a batch PDF with multiple offers.
        
        Args:
            offers: List of offer dictionaries
            template_html: HTML template with Jinja2 syntax
            layout_options: Layout configuration (pageSize, perPage, etc.)
            output_filename: Output PDF filename
            
        Returns:
            Path to generated PDF
        """
        try:
            layout_options = layout_options or {
                "pageSize": "A4",
                "perPage": 24,
                "orientation": "portrait"
            }
            
            # Prepare context with offers
            page_size_info = self._resolve_page_size(layout_options.get("pageSize"))
            context = {
                "offers": offers,
                "layout": layout_options,
                "total_offers": len(offers),
                "page_size_css": page_size_info["css"],
                "label_width": page_size_info["label_width"],
                "label_height": page_size_info["label_height"]
            }
            
            # Render template with offers
            rendered_html = self.render_template(template_html, context)
            
            # Generate PDF
            return await self.render_html_to_pdf(
                rendered_html,
                output_filename,
                page_size=page_size_info["pdf_size"]
            )
            
        except Exception as e:
            print(f"✗ Error generating batch PDF: {e}")
            raise

    def get_pdf_download_url(self, output_filename: str) -> str:
        """
        Get the relative URL for downloading a PDF.
        
        Args:
            output_filename: PDF filename
            
        Returns:
            Download URL path
        """
        return f"/downloads/pdfs/{output_filename}"


# Global PDF generator instance
pdf_service: Optional[PDFGeneratorService] = None


def init_pdf_service(output_dir: str = "./pdfs") -> PDFGeneratorService:
    """Initialize global PDF service instance"""
    global pdf_service
    pdf_service = PDFGeneratorService(output_dir)
    return pdf_service


def get_pdf_service() -> PDFGeneratorService:
    """Get the global PDF service instance"""
    if pdf_service is None:
        return init_pdf_service()
    return pdf_service
