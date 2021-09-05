# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class IsTypeContact(models.Model):
    _name = 'is.type.contact'
    _description = "Type de contact"
    _order = 'name'

    name = fields.Char("Type de contact", required=True, index=True)


class IsLoginExterne(models.Model):
    _name = 'is.login.externe'
    _description = "Login externe"
    _order = 'name'

    partner_id   = fields.Many2one('res.partner', 'Membre', required=True, index=True)
    name         = fields.Char("Login externe", required=True, index=True)
    mot_de_passe = fields.Char(u"Mot de passe outils externes")


class IsMotifDepart(models.Model):
    _name = 'is.motif.depart'
    _description = u"Motif de départ"
    _order = 'name'

    name = fields.Char(u"Motif de départ", required=True, index=True)


class IsCompetence(models.Model):
    _name = 'is.competence'
    _description = u"Compétence"
    _order = 'name'

    name = fields.Char(u"Compétence", required=True, index=True)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_prenom                 = fields.Char(u"Prénom")
    is_date_naissance         = fields.Date(u"Date de naissance")
    is_date_premiere_adhesion = fields.Date(u"Date de première adhésion")
    is_date_fin_adhesion      = fields.Date(u"Date de départ")
    is_motif_depart_id        = fields.Many2one('is.motif.depart', 'Motif de départ',index=True)
    is_groupe_ids             = fields.Many2many('is.groupe','is_groupe_membre_rel','partner_id','groupe_id', string="Membre des groupes")
    is_type_contact_ids       = fields.Many2many('is.type.contact','res_partner_type_contact_rel','partner_id','type_contact_id', string="Types de contact")
    is_competence_ids         = fields.Many2many('is.competence','res_partner_competence_rel','partner_id','competence_id', string="Compétences")
    is_trombinoscope          = fields.Boolean(u"J'accepte d'apparaître dans le trombinoscope")
    is_trombi_adresse         = fields.Boolean(u"Afficher mon addrese")
    is_trombi_tel_fixe        = fields.Boolean(u"Afficher mon téléphone fixe")
    is_trombi_tel_portable    = fields.Boolean(u"Afficher mon téléphone portable")
    is_trombi_mail            = fields.Boolean(u"Afficher mon email")



    @api.depends('is_company', 'name', 'parent_id.name', 'type', 'company_name','is_prenom')
    def _compute_display_name(self):
        diff = dict(show_address=None, show_address_only=None, show_email=None)
        names = dict(self.with_context(**diff).name_get())
        for partner in self:
            partner.display_name = names.get(partner.id)


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


    def _membership_state(self):
        """This Function return Membership State For Given Partner. """
        res = {}
        today = fields.Date.today()
        for partner in self:
            res[partner.id] = 'none'

            if partner.membership_cancel and today > partner.membership_cancel:
                res[partner.id] = 'free' if partner.free_member else 'canceled'
                continue
            if partner.membership_stop and today > partner.membership_stop:
                res[partner.id] = 'free' if partner.free_member else 'old'
                continue
            if partner.associate_member:
                res_state = partner.associate_member._membership_state()
                res[partner.id] = res_state[partner.associate_member.id]
                continue
            s = 4
            if partner.member_lines:
                for mline in partner.member_lines.sorted(key=lambda r: r.id):
                    if (mline.date_to or date.min) >= today and (mline.date_from or date.min) <= today:
                        if mline.account_invoice_line.invoice_id.partner_id == partner:
                            mstate = mline.account_invoice_line.invoice_id.state
                            if mstate == 'paid':
                                inv = mline.account_invoice_line.invoice_id
                                if inv.residual==0:
                                    s = 0
                                else:
                                    for ml in inv.payment_move_line_ids:
                                        if any(ml.invoice_id.filtered(lambda inv: inv.type == 'out_refund')):
                                            s = 2
                                        else:
                                            s = 0
                            elif mstate == 'open' and s != 0:
                                s = 1
                            elif mstate == 'cancel' and s != 0 and s != 1:
                                s = 2
                            elif mstate == 'draft' and s != 0 and s != 1:
                                s = 3
                        """
                            If we have a line who is in the period and paid,
                            the line is valid and can be used for the membership status.
                        """
                        if s == 0:
                            break
                if s == 4:
                    for mline in partner.member_lines:
                        if (mline.date_from or date.min) < today and (mline.date_to or date.min) < today and (mline.date_from or date.min) <= (mline.date_to or date.min) and mline.account_invoice_line and mline.account_invoice_line.invoice_id.state == 'paid':
                            s = 5
                        else:
                            s = 6
                if s == 0:
                    res[partner.id] = 'paid'
                elif s == 1:
                    res[partner.id] = 'invoiced'
                elif s == 2:
                    res[partner.id] = 'canceled'
                elif s == 3:
                    res[partner.id] = 'waiting'
                elif s == 5:
                    res[partner.id] = 'old'
                elif s == 6:
                    res[partner.id] = 'none'
            if partner.free_member and s != 0:
                res[partner.id] = 'free'
        return res
