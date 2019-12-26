# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class EventEvent(models.Model):
    _inherit = 'event.event'


    @api.depends('is_order_id')
    def _compute_facture_paye(self):
        for obj in self:
            facture = False
            if obj.is_order_id:
                facture = True
                paye    = True
                for line in obj.is_order_id.order_line:
                    if line.product_uom_qty>line.qty_invoiced:
                        facture = False
                    for invoice_line in line.invoice_lines:
                        if invoice_line.invoice_id.state!='paid':
                            paye=False
            if not facture:
                paye = False
            obj.is_facture = facture
            obj.is_paye    = paye


    name = fields.Char(string='Event', translate=False, required=True, readonly=False, states={'done': [('readonly', True)]})

    is_order_id      = fields.Many2one('sale.order', string='Devis')
    is_animateur_ids = fields.Many2many('res.partner','is_event_animateur_rel','event_id','partner_id', string="Animateurs")
    is_facture       = fields.Boolean(u'Facturé', compute='_compute_facture_paye', readonly=True, store=False)
    is_paye          = fields.Boolean(u'Payé'   , compute='_compute_facture_paye', readonly=True, store=False)

