import os
import unittest
from pathlib import Path

# Setup Django test environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()

from django.test import TestCase
from apps.portal.services import PortalService


class TestPortalService(TestCase):

    def test_bitacora_crud(self):
        # Obtener bitácora inicial
        bitacora = PortalService.obtener_bitacora()
        self.assertIn("texto", bitacora)
        self.assertIn("actualizado_en", bitacora)

        # Actualizar bitácora
        texto_prueba = "Novedad de prueba: Cambio de turno sin incidentes."
        res = PortalService.actualizar_bitacora(texto_prueba)
        self.assertEqual(res["status"], "ok")

        # Verificar que se actualizó
        bitacora_actualizada = PortalService.obtener_bitacora()
        self.assertEqual(bitacora_actualizada["texto"], texto_prueba)

    def test_asistentes(self):
        asistentes = PortalService.obtener_asistentes()
        self.assertIsInstance(asistentes, list)
        self.assertGreaterEqual(len(asistentes), 1)
        self.assertIn("nombre", asistentes[0])
        self.assertIn("telefono", asistentes[0])
        self.assertIn("correo", asistentes[0])

    def test_destinatarios_crud(self):
        destinatarios = PortalService.obtener_destinatarios()
        self.assertIsInstance(destinatarios, list)
        self.assertGreaterEqual(len(destinatarios), 1)

        # Crear destinatario
        res_crear = PortalService.crear_destinatario("TEST_EMPRESA", "test@empresa.com")
        self.assertEqual(res_crear["status"], "ok")
        nuevo_id = res_crear["destinatario"]["id"]

        # Verificar presencia
        destinatarios_nuevos = PortalService.obtener_destinatarios()
        creado = next((d for d in destinatarios_nuevos if d["id"] == nuevo_id), None)
        self.assertIsNotNone(creado)
        self.assertEqual(creado["correo"], "test@empresa.com")
        self.assertTrue(creado["activo"])

        # Toggle activo
        PortalService.toggle_destinatario(nuevo_id, False)
        dest_mod = PortalService.obtener_destinatarios()
        item_mod = next((d for d in dest_mod if d["id"] == nuevo_id), None)
        self.assertFalse(item_mod["activo"])

        # Eliminar destinatario
        res_del = PortalService.eliminar_destinatario(nuevo_id)
        self.assertEqual(res_del["status"], "ok")
        dest_final = PortalService.obtener_destinatarios()
        item_del = next((d for d in dest_final if d["id"] == nuevo_id), None)
        self.assertIsNone(item_del)

    def test_generador_correo_fin_semana(self):
        sab, dom, sem = PortalService.calcular_fechas_fin_semana_actual()
        self.assertTrue(len(sab) > 0)
        self.assertTrue(len(dom) > 0)
        self.assertIsInstance(sem, int)

        personal = {
            "nombre": "Hector Portillo",
            "cargo": "ASISTENTE DE SOPORTE",
            "telefono": "+56 9 8419 4843",
            "correo": "hector.portillo@innovex.cl"
        }

        html = PortalService.generar_html_correo_fin_semana(personal, sab, dom)
        self.assertIn("ASISTENCIA DE SOPORTE", html)
        self.assertIn("Hector Portillo", html)
        self.assertIn("+56 9 8419 4843", html)
        self.assertIn("hector.portillo@innovex.cl", html)
        self.assertIn("innovex", html)

    def test_trac_wiki_busqueda_e_indice(self):
        res_search = PortalService.buscar_trac_wiki("oxigeno")
        self.assertIn("results", res_search)
        self.assertGreaterEqual(len(res_search["results"]), 1)

        res_indice = PortalService.obtener_indice_trac_wiki()
        self.assertIn("indice", res_indice)
        self.assertIn("ANTENAS Y COMUNICACIÓN", res_indice["indice"])

    def test_estructura_personal(self):
        data = PortalService.obtener_estructura_personal()
        self.assertEqual(data["status"], "ok")
        self.assertIn("Rodrigo Bustamante", data["encargados"])
        self.assertIn("Manuel Yovera", data["encargados"])
        self.assertIn("Camilo Oyarzún", data["encargados"])
        self.assertIn("Francisco Vásquez", data["encargados"])

        # Zonas y Técnicos
        self.assertIn("Chiloé", data["todas_las_zonas"])
        self.assertIn("Pto. Montt", data["todas_las_zonas"])
        self.assertIn("Pto. Aguirre", data["todas_las_zonas"])
        self.assertIn("Melinka", data["todas_las_zonas"])

        # Mapa completo
        mapa = data["mapa_completo"]
        self.assertIn("Chiloé", mapa["Rodrigo Bustamante"]["zonas"])
        self.assertIn("Roger Vargas", mapa["Rodrigo Bustamante"]["tecnicos"])
        self.assertIn("Valdivia", mapa["Manuel Yovera"]["zonas"])
        self.assertIn("Armando Perez", mapa["Manuel Yovera"]["tecnicos"])

    def test_api_personal_estructura_view(self):
        from django.test import Client
        c = Client()
        response = c.get("/api/personal/estructura")
        self.assertEqual(response.status_code, 200)
        json_resp = response.json()
        self.assertEqual(json_resp["status"], "ok")
        self.assertIn("mapa_completo", json_resp)


if __name__ == "__main__":
    unittest.main()
