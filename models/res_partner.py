# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class IsTypeContact(models.Model):
    _name = 'is.type.contact'
    _description = "Type de contact"
    _order = 'name'

    name = fields.Char("Type de contact", required=True, index=True)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_prenom                 = fields.Char(u"Prénom")
    is_date_naissance         = fields.Date(u"Date de naissance")
    is_date_premiere_adhesion = fields.Date(u"Date de première adhésion")
    is_date_fin_adhesion      = fields.Date(u"Date de départ")
    is_motif_depart           = fields.Char(u"Motif de départ")
    is_login                  = fields.Char(u"Login outils externes")
    is_mot_de_passe           = fields.Char(u"Mot de passe outils externes")
    is_groupe_ids             = fields.Many2many('is.groupe','is_groupe_membre_rel','partner_id','groupe_id', string="Membre des groupes")
    is_type_contact_id        = fields.Many2one('is.type.contact', 'Type de contact',index=True)


    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        ids = []
        if name:
            ids = self._search(['|',('name', 'ilike', name),('is_prenom', 'ilike', name)] + args, limit=limit, access_rights_uid=name_get_uid)
        else:
            ids = self._search(args, limit=limit, access_rights_uid=name_get_uid)
        return self.browse(ids).name_get()


    def _get_name(self):
        """ Utility method to allow name_get to be overrided without re-browse the partner """
        partner = self
        name = partner.name or ''
        if partner.is_prenom:
            name = partner.is_prenom+u' '+name
        if partner.company_name or partner.parent_id:
            if not name and partner.type in ['invoice', 'delivery', 'other']:
                name = dict(self.fields_get(['type'])['type']['selection'])[partner.type]
            if not partner.is_company:
                name = "%s, %s" % (partner.commercial_company_name or partner.parent_id.name, name)
        if self._context.get('show_address_only'):
            name = partner._display_address(without_company=True)
        if self._context.get('show_address'):
            name = name + "\n" + partner._display_address(without_company=True)
        name = name.replace('\n\n', '\n')
        name = name.replace('\n\n', '\n')
        if self._context.get('address_inline'):
            name = name.replace('\n', ', ')
        if self._context.get('show_email') and partner.email:
            name = "%s <%s>" % (name, partner.email)
        if self._context.get('html_format'):
            name = name.replace('\n', '<br/>')
        if self._context.get('show_vat') and partner.vat:
            name = "%s ‒ %s" % (name, partner.vat)
        return name


