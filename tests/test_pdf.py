from src.services.certificado_service import (
    CertificadoService
)

from src.pdf.generador_pdf import (
    GeneradorPDF
)


def main():

    certificado = (
        CertificadoService.cargar_certificado(
            "inn-test2",
            2026
        )
    )
    print(certificado["datos_generales"]["location"])
    print(certificado["datos_generales"]["nombre_centro"])
    
    GeneradorPDF().generar(
        certificado,
        "output/prueba.pdf"
    )


if __name__ == "__main__":
    main()