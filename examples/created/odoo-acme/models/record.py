from odoo import fields, models


class AcmeOperaO(models.Model):
    _name = "forja.acme_opera_o"
    _description = 'Acme Operação'

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
