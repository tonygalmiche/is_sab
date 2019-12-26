# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import Warning


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    @api.onchange('product_id')
    def _onchange_product_id(self):
        res = super(AccountInvoiceLine, self)._onchange_product_id()
        if self.product_id.is_account_analytic_id and not self.account_analytic_id:
            self.account_analytic_id = self.product_id.is_account_analytic_id.id
        return res


    @api.model
    def create(self, vals):
        res = super(AccountInvoiceLine, self).create(vals)
        res._onchange_product_id()
        return res
