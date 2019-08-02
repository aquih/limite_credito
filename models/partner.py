# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging

class Partner(models.Model):
    _inherit = 'res.partner'

    dias_gracia = fields.Integer('Días de gracia')
