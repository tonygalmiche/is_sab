# -*- coding: utf-8 -*-

from odoo import api, fields, models
import time
import datetime
from dateutil.relativedelta import relativedelta



class IsEventRecurrentWizard(models.TransientModel):
    _name = 'is.event.reccurent.wizard'
    _description = u"Récurrence des évènements"

    periodicite = fields.Selection([('jour', 'Jour'), ('semaine', 'Semaine'), ('mois', 'Mois')], u"Périodicité", required=True)
    nb_creation = fields.Integer(u"Nombre d'évènements à créer", required=True)


    @api.multi
    def reccurence_action(self):
        cr , uid, context = self.env.args
        for obj in self:
            ids=[]
            if 'active_id' in context:
                event_id = context['active_id']
                event = self.env['event.event'].browse(event_id)
                date_begin = event.date_begin
                date_end   = event.date_end
                ids.append(event.id)
                for line in range(obj.nb_creation):
                    if obj.periodicite=='jour':
                        date_end   = date_end + datetime.timedelta(days=1)
                        date_begin = date_begin + datetime.timedelta(days=1)
                    if obj.periodicite=='semaine':
                        date_end   = date_end + datetime.timedelta(days=7)
                        date_begin = date_begin + datetime.timedelta(days=7)
                    if obj.periodicite=='mois':
                        date_end   = date_end + relativedelta(months=+1)
                        date_begin = date_begin + relativedelta(months=+1)
                    copy = event.copy()
                    vals={
                        'name'      : event.name,
                        'date_begin': date_begin,
                        'date_end'  : date_end,
                    }
                    copy.write(vals)
                    ids.append(copy.id)
            return {
                'name': u'Evènements récurrents',
                'view_mode': 'tree,form',
                'view_type': 'form',
                'res_model': 'event.event',
                'domain': [
                    ('id','in',ids),
                ],
                'type': 'ir.actions.act_window',
            }

