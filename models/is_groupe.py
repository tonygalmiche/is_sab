# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import Warning


class IsGroupe(models.Model):
    _name = 'is.groupe'
    _description = "Groupe"
    _order = 'name'

    name            = fields.Char("Nom du groupe", required=True, index=True)
    responsable_ids = fields.Many2many('res.partner','is_groupe_responsable_rel','groupe_id','partner_id', string="Responsables")
    membre_ids      = fields.Many2many('res.partner','is_groupe_membre_rel'     ,'groupe_id','partner_id', string="Membres")




    #users     = fields.Many2many('res.users' , 'res_groups_users_rel', 'gid', 'uid')
    #groups_id = fields.Many2many('res.groups', 'res_groups_users_rel', 'uid', 'gid', string='Groups', default=_default_groups)
