# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import Warning
from datetime import datetime, timedelta


class IsGenreLivre(models.Model):
    _name = 'is.genre.livre'
    _description = "Genre de livre"
    _order = 'name'

    name = fields.Char("Genre de livre", required=True, index=True)


class IsLivre(models.Model):
    _name = 'is.livre'
    _description = u"Livre"
    _order = 'name'

    @api.depends('pret_ids')
    def _compute(self):
        for obj in self:
            date_debut  = False
            date_fin    = False
            date_retour = False
            for p in obj.pret_ids:
                date_debut  = p.date_debut
                date_fin    = p.date_fin
                date_retour = p.date_retour
            if not date_fin and date_debut:
                date_fin = date_debut + timedelta(days=14)
            obj.date_debut  = date_debut
            obj.date_fin    = date_fin
            obj.date_retour = date_retour

    name             = fields.Char(u"Titre du livre", required=True, index=True)
    reference        = fields.Char(u"Référence")
    auteur           = fields.Char(u"Auteur")
    date_publication = fields.Date(u"Date de publication")
    editeur          = fields.Char(u"Editeur")
    genre_livre_id   = fields.Many2one('is.genre.livre', u'Genre de livre', required=True,index=True)
    pret_ids         = fields.One2many('is.livre.pret', 'livre_id', u'Prêts')
    date_debut       = fields.Date(u"Date de début", compute='_compute', readonly=True, store=True)
    date_fin         = fields.Date(u"Date de fin"  , compute='_compute', readonly=True, store=True)
    date_retour      = fields.Date(u"Date de retour", compute='_compute', readonly=True, store=True)


class IsLivrePret(models.Model):
    _name = 'is.livre.pret'
    _description = u"Prêts du livre"
    _order = 'date_debut'

    livre_id    = fields.Many2one('is.livre', 'Matériel' , required=True, ondelete='cascade')
    membre_id   = fields.Many2one('res.partner', 'Membre'   , required=True)
    date_debut  = fields.Date("Date de début", required=True, index=True)
    date_fin    = fields.Date("Date de fin")
    date_retour = fields.Date("Date de retour")
    note        = fields.Text("Note")



