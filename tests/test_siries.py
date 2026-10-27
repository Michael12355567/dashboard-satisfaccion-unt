import unittest
from unittest.mock import Mock, patch
import requests
from ura_api import URAClient, URAError, BASE_URL
from reportes import tabla, calidad, resumen, excel
from seguridad import HASHER

class ClientTests(unittest.TestCase):
    def setUp(self):
        self.c = URAClient("DEMO_NO_REAL_TOKEN")

    def test_url_catalogo_y_headers(self):
        response = Mock(status_code=200, headers={})
        response.iter_content.return_value = [b'{"periodos":{"2025-2":{}},"escuelas":[],"sedes":[]}']
        cm = self.c.session.request
        with patch.object(self.c.session, 'request') as req:
            req.return_value.__enter__.return_value = response
            resultado = self.c.catalogos()
            self.assertIn('2025-2', resultado['periodos'])
            args, kwargs = req.call_args
            self.assertEqual(args[1], BASE_URL + '/api/reportes/siries/catalogos')
            self.assertFalse(kwargs['allow_redirects'])
            self.assertTrue(kwargs['verify'])

    def test_401_no_expone_token(self):
        response = Mock(status_code=401, headers={})
        with patch.object(self.c.session, 'request') as req:
            req.return_value.__enter__.return_value = response
            with self.assertRaises(URAError) as err:
                self.c.catalogos()
            self.assertNotIn('DEMO_NO_REAL_TOKEN', str(err.exception))

    def test_validacion_id(self):
        with self.assertRaises(URAError):
            self.c.estado('https://malicioso.com')

    def test_pregrado_filtro(self):
        with patch.object(self.c, '_json', return_value={'id':'00000000-0000-4000-8000-000000000001','estado':'pendiente'}) as req:
            self.c.crear_pregrado('siries_matriculados_pregrado', ['2025-2'], escuelas=[], sedes=[])
            self.assertEqual(req.call_args.kwargs['payload']['filtros'], {'periodos':['2025-2']})
            self.assertTrue(req.call_args.kwargs['headers']['Idempotency-Key'])

class DataTests(unittest.TestCase):
    def setUp(self):
        self.filas = [{'tipo_documento':'DNI','nro_documento':'01234567','carrera':'A','genero':'FEMENINO','discapacitado':None},
                      {'tipo_documento':'DNI','nro_documento':'BAD','carrera':'A','genero':'MASCULINO','discapacitado':None}]

    def test_calidad(self):
        q = calidad(tabla(self.filas))
        self.assertEqual(q['dni_invalidos'], 1)
        self.assertNotIn('discapacitado', q['nulos'].get('campo', []).tolist() if not q['nulos'].empty else [])

    def test_excel(self):
        data = excel(self.filas, [{'campo':'nro_documento','codigo':'dni_invalido'}], {'tipo':'prueba'})
        self.assertTrue(data.startswith(b'PK'))
        self.assertGreater(len(data), 1000)

    def test_excel_formula_escape(self):
        from reportes import _sin_formula
        self.assertEqual(_sin_formula('=HYPERLINK("http://bad")'), "'=HYPERLINK(\"http://bad\")")

if __name__ == '__main__':
    unittest.main()
