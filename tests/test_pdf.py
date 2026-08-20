import os
import unittest
from pathlib import Path

# Setup Django test environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()

from apps.certificados.services import CertificadoService
from apps.core.pdf.generador_pdf import GeneradorPDF


class TestGeneradorPDF(unittest.TestCase):

    def test_generar_pdf_basico(self):
        cert = CertificadoService.crear_certificado("test-loc", "Centro Test")
        output_dir = Path("output")
        output_dir.mkdir(parents=True, exist_ok=True)
        pdf_path = output_dir / "test_output.pdf"

        GeneradorPDF().generar(cert, str(pdf_path))
        self.assertTrue(pdf_path.exists())
        self.assertGreater(pdf_path.stat().st_size, 1000)

        # Cleanup
        if pdf_path.exists():
            pdf_path.unlink()


if __name__ == "__main__":
    unittest.main()