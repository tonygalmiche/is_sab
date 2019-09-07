# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import Warning
from datetime import datetime, timedelta


class IsTypeMateriel(models.Model):
    _name = 'is.type.materiel'
    _description = "Type de matériel"
    _order = 'name'

    name = fields.Char("Type de matériel", required=True, index=True)


class IsMateriel(models.Model):
    _name = 'is.materiel'
    _description = u"Matériel"
    _order = 'name'

    @api.depends('pret_ids')
    def _compute(self):
        for obj in self:
            date_debut = False
            date_fin   = False
            for p in obj.pret_ids:
                date_debut = p.date_debut
                date_fin   = p.date_fin
            #if not date_fin and date_debut:
            #    date_fin = date_debut + timedelta(days=365)
            obj.date_debut = date_debut
            obj.date_fin   = date_fin 


    name             = fields.Char("Nom", required=True, index=True)
    type_materiel_id = fields.Many2one('is.type.materiel', 'Type de matériel', required=True,index=True)
    pret_ids         = fields.One2many('is.materiel.pret', 'materiel_id', u'Prêts')
    date_debut       = fields.Date("Date de début", compute='_compute', readonly=True, store=True)
    date_fin         = fields.Date("Date de fin"  , compute='_compute', readonly=True, store=True)



class IsMaterielPret(models.Model):
    _name = 'is.materiel.pret'
    _description = u"Prêts du matériel"
    _order = 'date_debut'

    materiel_id = fields.Many2one('is.materiel', 'Matériel' , required=True, ondelete='cascade')
    event_id    = fields.Many2one('event.event', 'Evénement', required=True)
    membre_id   = fields.Many2one('res.partner', 'Membre'   , required=True)
    date_debut  = fields.Date("Date de début", required=True, index=True)
    date_fin    = fields.Date("Date de fin")




