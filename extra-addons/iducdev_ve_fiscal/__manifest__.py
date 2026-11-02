# Part of IDUCDEV. See LICENSE file for full copyright and licensing details.
{
    "name": "Venezuela - Datos fiscales SENIAT",
    "summary": (
        "Número de control, fecha y hora de emisión y total en bolívares "
        "exigidos por la Providencia Administrativa SNAT/2026/00093"
    ),
    "description": """
Venezuela - Datos fiscales SENIAT
=================================

Anade a las facturas de cliente los datos que exige la Providencia
Administrativa SNAT/2026/00093 (Gaceta Oficial N. 43.484 del 21/10/2026,
vigente a los 180 dias continuos de su publicacion): numero de control,
numero de factura del medio autorizado, fecha y hora de emision fiscal,
medio de emision, tipo de cambio y total en bolivares, marca (E) en las
lineas exentas y frase de emision conforme a la Providencia.

El modulo no emite documentos fiscales: registra los que se emiten por el
portal del SENIAT o por un proveedor autorizado. Odoo sigue siendo el
sistema de gestion comercial.

La exigencia de los datos al validar es opcional y se activa desde
Ajustes > Contabilidad, para poder seguir trabajando con normalidad hasta
la entrada en vigencia.
""",
    "version": "19.0.1.0.0",
    "category": "Accounting/Localizations",
    "author": "IDUCDEV",
    "website": "https://www.iducdev.org",
    "license": "LGPL-3",
    "depends": ["account"],
    "data": [
        "data/res_country_data.xml",
        "views/account_move_views.xml",
        "views/res_config_settings_views.xml",
        "report/report_invoice.xml",
    ],
    "installable": True,
    "application": False,
}
