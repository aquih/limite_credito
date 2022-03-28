# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.release import version_info

import datetime
import logging

class SaleOrder(models.Model):
    _inherit = "sale.order"


    def _limite_credito(self):
        if self.partner_id.credit_limit > 0 and self.partner_id.credit + self.amount_total > self.partner_id.credit_limit + self.partner_id.extra_financiamiento:
            raise UserError(_('No puede sobrepasar el límite de crédito'))

    def _facturas_vencidas(self):
        hoy = datetime.datetime.today()
        if self.partner_id.dias_gracia > 0:
            fecha_vencimiento = datetime.date(hoy.year, hoy.month, hoy.day) - datetime.timedelta(days=self.partner_id.dias_gracia)
        else:
            fecha_vencimiento = datetime.date(hoy.year, hoy.month, hoy.day) - datetime.timedelta(days=1)
        
        if version_info[0] == 14 or version_info[0] == 15:
            facturas_vencidas = self.env['account.move'].search([('move_type', '=', 'out_invoice'), ('partner_id', '=', self.partner_id.id), ('state', '=', 'posted'), ('payment_state', '!=', 'paid'), ('invoice_date_due', '<=', fecha_vencimiento)])
        else:
            facturas_vencidas = self.env['account.move'].search([('type', '=', 'out_invoice'), ('partner_id', '=', self.partner_id.id), ('state', '=', 'posted'), ('invoice_payment_state', '!=', 'paid'), ('invoice_date_due', '<=', fecha_vencimiento)])
            
        if facturas_vencidas:
            raise UserError(_('El cliente tiene facturas vencidas'))
    
    def action_confirm(self):
        if not self.user_has_groups('sales_team.group_sale_manager'):
            self._limite_credito()
            if not self.partner_id.no_facturas_vencidas:
                self._facturas_vencidas()
        super(SaleOrder, self).action_confirm()
        return True
