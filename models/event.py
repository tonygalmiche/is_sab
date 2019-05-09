# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class EventEvent(models.Model):
    _inherit = 'event.event'


    is_order_id = fields.Many2one('sale.order', string='Devis')



