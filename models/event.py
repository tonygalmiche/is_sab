# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class EventEvent(models.Model):
    _inherit = 'event.event'


    is_order_id      = fields.Many2one('sale.order', string='Devis')
    is_animateur_ids = fields.Many2many('res.partner','is_event_animateur_rel','event_id','partner_id', string="Animateurs")
    is_facture       = fields.Boolean(u'Facturé')
    is_paye          = fields.Boolean(u'Payé')


