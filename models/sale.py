# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

import datetime
import logging

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _limite_credito(self):
        # Accesar credit_limit requiere permisos de facturacion que no queremos dar a usaurios normales
        cliente_id = self.sudo().partner_id
        if cliente_id.credit_limit > 0 and cliente_id.credit + self.amount_total > cliente_id.credit_limit + cliente_id.extra_financiamiento:
            raise UserError(_('No puede sobrepasar el límite de crédito.'))

    def _facturas_vencidas(self):
        hoy = datetime.date.today()
        if self.partner_id.dias_gracia > 0:
            fecha_vencimiento = hoy - datetime.timedelta(days=self.partner_id.dias_gracia)
        else:
            fecha_vencimiento = hoy - datetime.timedelta(days=1)
        
        facturas_vencidas = self.env['account.move'].search([('move_type', '=', 'out_invoice'), ('partner_id', '=', self.partner_id.id), ('state', '=', 'posted'), ('payment_state', 'not in', ['paid', 'in_payment', 'reversed']), ('invoice_date_due', '<=', fecha_vencimiento)])            
        if facturas_vencidas:
            raise UserError(_('El cliente tiene facturas vencidas.'))
    
    def action_confirm(self):
        if not self.env.user.has_group('sales_team.group_sale_manager'):
            self._limite_credito()
            if not self.partner_id.no_facturas_vencidas:
                self._facturas_vencidas()
        super(SaleOrder, self).action_confirm()
        return True
