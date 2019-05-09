# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class IsTypeProduction(models.Model):
    _name = 'is.type.production'
    _description = "Type de production"
    _order = 'name'

    name = fields.Char("Type de production", required=True, index=True)


class IsLangue(models.Model):
    _name = 'is.langue'
    _description = u"Langue parlée"
    _order = 'name'

    name = fields.Char("Langue parlée", required=True, index=True)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_type_production_ids  = fields.Many2many('is.type.production', 'res_partner_type_production_rel', 'partner_id', 'type_production_id', u'Type de production')
    is_num_client           = fields.Char(u"Notre numéro client")
    is_date_briefing        = fields.Date(u"Date briefing facturation")
    is_coordonnee_gps       = fields.Char(u"Coordonnées GPS")
    is_coordonnee_gps_metha = fields.Char(u"Coordonnées GPS site de métha")
    is_comment_commande     = fields.Text(u"Commentaire commande")
    is_comment_livraison    = fields.Text(u"Commentaire livraison")
    is_comment_remise       = fields.Text(u"Commentaire remise")
    is_comment_reglement    = fields.Text(u"Conditions de règlement")
    is_comment_conges       = fields.Text(u"Congés (ouverture / fermeture)")
    is_langue_parlee_ids    = fields.Many2many('is.langue', 'res_partner_langue_rel', 'partner_id', 'langue_id', u'Langues parlées')

