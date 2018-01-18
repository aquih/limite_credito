# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

class SaleOrder(models.Model):
    _inherit = "sale.order"

    
    @api.multi
    def action_confirm(self):
        super(SaleOrder, self).action_confirm()
        if self.partner_id.credit + self.amount_total > self.partner_id.credit_limit:
            raise UserError(_('No puede sobrepasar el limite de credito'))
        return True
