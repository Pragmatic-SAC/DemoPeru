# -*- coding: utf-8 -*-
{
    "name": "Restrict Create Edit Link by Model",
    "category": "Tools",
    "summary": "Restrict links to create, edit,delete, create from view by model and user..",
    "version": "14.0.1",
    "license": "OPL-1",
    "website": "https://www.pragmatic.com.pe/",
    "contributors": [
        "Kelvin Meza <kmeza@pragmatic.com.pe>",
    ],
    "depends": ["base"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/ir_model.xml",
        "views/template.xml"
    ],
    "images": [
        'static/description/banner.gif'
    ],
    "author": "Pragmatic S.A.C",
    "website": "pragmatic.com.pe",
    "maintainer": "Pragmatic S.A.C.",
    "installable": True,
    "auto_install": False,
    "application": True,
}
