# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_account_analytic_id = fields.Many2one('account.analytic.account', "Section analytique")


