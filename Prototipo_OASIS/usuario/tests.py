from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
import os

class ManualUsuarioTests(TestCase):
    
    def setUp(self):
        self.client = Client()
    
    def test_manual_usuario_view(self):
        '''Prueba que la vista del manual carga correctamente'''
        response = self.client.get(reverse('auth:manual_usuario'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manual_usuario.html')
    
    def test_descargar_pdf_existe(self):
        '''Prueba que el archivo PDF existe'''
        pdf_path = os.path.join(settings.MEDIA_ROOT, 'docs', 'MANUAL_DE_USUARIO_OASIS.pdf')
        self.assertTrue(os.path.exists(pdf_path), "El PDF no existe en la ruta especificada")
    
    def test_descargar_pdf_response(self):
        '''Prueba que la descarga del PDF funciona'''
        response = self.client.get(reverse('auth:descargar_manual_pdf'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('attachment', response['Content-Disposition'])