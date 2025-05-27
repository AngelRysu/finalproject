import unittest
from src.utils import extraer_palabras, calcular_coincidencias, cumple_umbral, stopwords

class TestUtils(unittest.TestCase):

    def test_extraer_palabras_basico(self):
        text = "Hello world, this is a test!"
        expected_words = {"hello", "world", "test"} # "this", "is", "a" son stopwords
        self.assertEqual(extraer_palabras(text, stopwords), expected_words)

    def test_extraer_palabras_con_numeros_y_puntuacion(self):
        text = "Python 3.9 is awesome! (Version 2)"
        expected_words = {"python", "3", "9", "awesome", "version", "2"}
        self.assertEqual(extraer_palabras(text, stopwords), expected_words)

    def test_extraer_palabras_texto_vacio(self):
        text = ""
        expected_words = set()
        self.assertEqual(extraer_palabras(text, stopwords), expected_words)

    def test_extraer_palabras_solo_stopwords(self):
        text = "The quick brown fox jumps over the lazy dog" # Algunas son stopwords
        expected_words = {"quick", "brown", "fox", "jumps", "over", "lazy", "dog"}
        self.assertEqual(extraer_palabras(text, stopwords), expected_words)

    def test_calcular_coincidencias_completas(self):
        desc_words = {"python", "django", "flask", "aws"}
        cv_words = {"python", "django", "docker", "linux"}
        expected_coincidences = {"python", "django"}
        self.assertEqual(calcular_coincidencias(desc_words, cv_words), expected_coincidences)

    def test_calcular_coincidencias_sin_coincidencias(self):
        desc_words = {"java", "spring"}
        cv_words = {"python", "django"}
        expected_coincidences = set()
        self.assertEqual(calcular_coincidencias(desc_words, cv_words), expected_coincidences)

    def test_calcular_coincidencias_desc_vacia(self):
        desc_words = set()
        cv_words = {"python", "django"}
        expected_coincidences = set()
        self.assertEqual(calcular_coincidencias(desc_words, cv_words), expected_coincidences)

    def test_calcular_coincidencias_cv_vacio(self):
        desc_words = {"java", "spring"}
        cv_words = set()
        expected_coincidences = set()
        self.assertEqual(calcular_coincidencias(desc_words, cv_words), expected_coincidences)

    def test_cumple_umbral_positivo(self):
        coincidences = {"skill1", "skill2"}
        total = 3
        umbral = 0.6
        self.assertTrue(cumple_umbral(coincidences, total, umbral)) # 2/3 = 0.66... >= 0.6

    def test_cumple_umbral_negativo(self):
        coincidences = {"skill1"}
        total = 3
        umbral = 0.6
        self.assertFalse(cumple_umbral(coincidences, total, umbral)) # 1/3 = 0.33... < 0.6

    def test_cumple_umbral_total_cero(self):
        coincidences = {"skill1", "skill2"}
        total = 0
        umbral = 0.5
        self.assertFalse(cumple_umbral(coincidences, total, umbral))

    def test_cumple_umbral_cero_coincidencias(self):
        coincidences = set()
        total = 5
        umbral = 0.1
        self.assertFalse(cumple_umbral(coincidences, total, umbral))

    def test_cumple_umbral_exacto(self):
        coincidences = {"skill1", "skill2", "skill3"}
        total = 5
        umbral = 0.6
        self.assertTrue(cumple_umbral(coincidences, total, umbral)) # 3/5 = 0.6 >= 0.6

if __name__ == '__main__':
    unittest.main()