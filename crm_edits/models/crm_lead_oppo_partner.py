# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pytz
import threading
from collections import OrderedDict, defaultdict
from datetime import date, datetime, timedelta
from psycopg2 import sql

from odoo import api, fields, models, tools, SUPERUSER_ID
from odoo.addons.iap.tools import iap_tools
from odoo.addons.mail.tools import mail_validation
from odoo.addons.phone_validation.tools import phone_validation
from odoo.exceptions import UserError, AccessError
from odoo.osv import expression
from odoo.tools.translate import _
from odoo.tools import date_utils, email_re, email_split, is_html_empty, groupby
from odoo.tools.misc import get_lang


class Lead2OpportunityPartnerInherit(models.TransientModel):
    _inherit = 'crm.lead2opportunity.partner'

    expected_revenue = fields.Monetary('Expected Revenue', currency_field='company_currency', tracking=True,
                                       related='lead_id.expected_revenue')
    company_currency = fields.Many2one("res.currency", string='Currency', compute="_compute_company_currency",
                                       compute_sudo=True)
    company_id = fields.Many2one(
        'res.company', string='Company', index=True,
        related='lead_id.company_id', readonly=False, store=True)

    reference = fields.Char(related='lead_id.reference')
    account_manager_id = fields.Many2one('res.users', related='lead_id.account_manager_id')
    appraisals_id = fields.Many2one('res.users', related='lead_id.appraisals_id')
    poc = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')],
        related='lead_id.poc')
    existing_market_place = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')],
        related='lead_id.existing_market_place'
    )

    @api.depends('company_id')
    def _compute_company_currency(self):
        for lead in self:
            if not lead.company_id:
                lead.company_currency = self.env.company.currency_id
            else:
                lead.company_currency = lead.company_id.currency_id

    def _action_merge(self):
        to_merge = self.duplicated_lead_ids
        result_opportunity = to_merge.merge_opportunity(auto_unlink=False)
        result_opportunity.action_unarchive()

        if result_opportunity.type == "lead":
            self._convert_and_allocate(result_opportunity, [self.user_id.id], team_id=self.team_id.id,
                                       expected_revenue=self.expected_revenue,
                                       reference=self.reference,
                                       account_manager_id=self.account_manager_id.id,
                                       appraisals_id=self.appraisals_id.id,
                                       poc=self.poc,
                                       existing_market_place=self.existing_market_place,
                                       )
        else:
            if not result_opportunity.user_id or self.force_assignment:
                result_opportunity.write({
                    'user_id': self.user_id.id,
                    'team_id': self.team_id.id,
                    'expected_revenue': self.expected_revenue,
                    'reference': self.reference,
                    'account_manager_id': self.account_manager_id,
                    'appraisals_id': self.appraisals_id,
                })
        (to_merge - result_opportunity).sudo().unlink()
        return result_opportunity

    def _action_convert(self):
        """ """
        result_opportunities = self.env['crm.lead'].browse(self._context.get('active_ids', []))
        self._convert_and_allocate(result_opportunities, [self.user_id.id], team_id=self.team_id.id,
                                   expected_revenue=self.expected_revenue,
                                   reference=self.reference,
                                   account_manager_id=self.account_manager_id.id,
                                   appraisals_id=self.appraisals_id.id,
                                   )
        return result_opportunities[0]

    def _action_convert(self):
        """ """
        result_opportunities = self.env['crm.lead'].browse(self._context.get('active_ids', []))
        self._convert_and_allocate(result_opportunities, [self.user_id.id], team_id=self.team_id.id,
                                   )
        return result_opportunities[0]
