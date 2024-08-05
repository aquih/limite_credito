# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging

class Partner(models.Model):
    _inherit = 'res.partner'

    dias_gracia = fields.Integer('Días de gracia', groups='account.group_account_readonly')
    extra_financiamiento = fields.Float(string='Extra financiamiento', groups='account.group_account_readonly')
    no_facturas_vencidas = fields.Boolean(string='No validar facturas vencidas', groups='account.group_account_readonly')
