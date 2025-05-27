import unittest
import os
from unittest.mock import patch, MagicMock
from src.pdf_processor import procesar_pdf
from src.utils import stopwords, extraer_palabras # Importar stopwords para las pruebas

class TestPdfProcessor(unittest.TestCase):

    @patch('src.pdf_processor.extract_text') # Mockea la función extract_text de pdfminer.high_level
    def test_procesar_pdf_cumple_umbral(self, mock_extract_text):
        # Configurar el mock para que devuelva un texto específico
        mock_extract_text.return_value = "This CV has Python, Django, and AWS skills."

        # MODIFICACIÓN CLAVE AQUÍ: Aseguramos que la descripción contenga solo las palabras que SÍ están en el CV,
        # para que el umbral de 70% se cumpla (3 de 3 palabras = 100% coincidencia)
        palabras_desc = extraer_palabras("Looking for Python, Django, AWS.", stopwords)

        # Ejecutar la función a probar
        result = procesar_pdf("test_cv.pdf", "/fake/path", palabras_desc, 0.7)

        # Verificar que la función devolvió algo (cumplió el umbral)
        self.assertIsNotNone(result)
        filename, coincidences, text_content = result
        self.assertEqual(filename, "test_cv.pdf")
        self.assertEqual(coincidences, {"python", "django", "aws"})
        self.assertIn("Python, Django, and AWS skills", text_content)

        # Asegurarse de que extract_text fue llamado
        mock_extract_text.assert_called_once_with(os.path.join("/fake/path", "test_cv.pdf"))

    @patch('src.pdf_processor.extract_text')
    def test_procesar_pdf_no_cumple_umbral(self, mock_extract_text):
        mock_extract_text.return_value = "This CV has Java skills."
        palabras_desc = extraer_palabras("Looking for Python, Django, AWS.", stopwords)

        result = procesar_pdf("test_cv2.pdf", "/fake/path", palabras_desc, 0.7) # 0 de 3 = 0 < 0.7

        self.assertIsNone(result)

    @patch('src.pdf_processor.extract_text')
    def test_procesar_pdf_error_lectura(self, mock_extract_text):
        # Simular un error al leer el PDF
        mock_extract_text.side_effect = Exception("File corrupted")

        palabras_desc = extraer_palabras("Python developer", stopwords)

        result = procesar_pdf("corrupt_cv.pdf", "/fake/path", palabras_desc, 0.5)

        self.assertIsNone(result) # Debería devolver None si hay un error

if __name__ == '__main__':
    unittest.main()