# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'


    is_prenom                 = fields.Char(u"Prénom")
    is_date_naissance         = fields.Date(u"Date de naissance")
    is_date_premiere_adhesion = fields.Date(u"Date de première adhésion")
    is_date_fin_adhesion      = fields.Date(u"Date de fin d'adhésion")
    is_login                  = fields.Char(u"Login outils externes")
    is_mot_de_passe           = fields.Char(u"Mot de passe outils externes")

