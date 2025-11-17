"""
Storage service module.
Handles file uploads, storage, and management.
"""

import os
import shutil
import zipfile
from pathlib import Path
from typing import Optional, Tuple
from datetime import datetime


class StorageService:
    """Service for managing file storage and uploads"""

    def __init__(self, base_dir: str = "./uploads"):
        """
        Initialize storage service.
        
        Args:
            base_dir: Base directory for all uploads
        """
        self.base_dir = Path(base_dir)
        self.csv_dir = self.base_dir / "csv"
        self.templates_dir = self.base_dir / "templates"
        self.pdfs_dir = self.base_dir / "pdfs"
        
        # Create directories
        self._ensure_directories()

    def _ensure_directories(self):
        """Create all necessary directories"""
        self.csv_dir.mkdir(parents=True, exist_ok=True)
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.pdfs_dir.mkdir(parents=True, exist_ok=True)

    async def save_csv_file(self, file_content: bytes, filename: str) -> str:
        """
        Save uploaded CSV file.
        
        Args:
            file_content: File bytes
            filename: Original filename
            
        Returns:
            Saved file path
        """
        try:
            # Add timestamp to avoid conflicts
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_filename = f"{timestamp}_{filename}"
            file_path = self.csv_dir / safe_filename
            
            with open(file_path, "wb") as f:
                f.write(file_content)
            
            print(f"✓ CSV file saved: {file_path}")
            return str(file_path)
            
        except Exception as e:
            print(f"✗ Error saving CSV file: {e}")
            raise

    async def save_template_zip(self, file_content: bytes, template_name: str) -> Tuple[str, str]:
        """
        Save and extract template ZIP file.
        
        Args:
            file_content: ZIP file bytes
            template_name: Name for the template
            
        Returns:
            Tuple of (extracted_dir_path, html_file_path or None)
        """
        try:
            # Create template directory
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            template_dir = self.templates_dir / f"{template_name}_{timestamp}"
            template_dir.mkdir(parents=True, exist_ok=True)
            
            # Save ZIP and extract
            zip_path = template_dir / "template.zip"
            with open(zip_path, "wb") as f:
                f.write(file_content)
            
            # Extract ZIP
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(template_dir)
            
            # Find HTML file
            html_file = None
            for file in template_dir.glob("*.html"):
                html_file = str(file)
                break
            
            print(f"✓ Template extracted: {template_dir}")
            return str(template_dir), html_file
            
        except Exception as e:
            print(f"✗ Error saving template ZIP: {e}")
            raise

    async def read_template_file(self, file_path: str) -> str:
        """
        Read template file content.
        
        Args:
            file_path: Path to template file
            
        Returns:
            File content as string
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"✗ Error reading template file: {e}")
            raise

    def get_pdf_path(self, filename: str) -> str:
        """
        Get full path for PDF storage.
        
        Args:
            filename: PDF filename
            
        Returns:
            Full path to PDF
        """
        return str(self.pdfs_dir / filename)

    def cleanup_old_files(self, days: int = 7):
        """
        Clean up files older than specified days.
        
        Args:
            days: Age threshold in days
        """
        try:
            import time
            current_time = time.time()
            cutoff_time = current_time - (days * 86400)
            
            for directory in [self.csv_dir, self.templates_dir, self.pdfs_dir]:
                for file_path in directory.glob("*"):
                    if file_path.stat().st_mtime < cutoff_time:
                        if file_path.is_file():
                            file_path.unlink()
                        elif file_path.is_dir():
                            shutil.rmtree(file_path)
                        print(f"✓ Cleaned up: {file_path}")
        except Exception as e:
            print(f"⚠ Cleanup warning: {e}")


# Global storage instance
storage_service: Optional[StorageService] = None


def init_storage_service(base_dir: str = "./uploads") -> StorageService:
    """Initialize global storage service instance"""
    global storage_service
    storage_service = StorageService(base_dir)
    return storage_service


def get_storage_service() -> StorageService:
    """Get the global storage service instance"""
    if storage_service is None:
        return init_storage_service()
    return storage_service
