# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pytz
import threading
from collections import OrderedDict, defaultdict
from datetime import date, datetime, timedelta
from psycopg2 import sql

from odoo import api, fields, models, tools
from odoo.addons.iap.tools import iap_tools
from odoo.addons.mail.tools import mail_validation
from odoo.addons.phone_validation.tools import phone_validation
from odoo.exceptions import UserError, AccessError
from odoo.osv import expression
from odoo.tools.translate import _
from odoo.tools import date_utils, email_re, email_split, is_html_empty, groupby
from odoo.tools.misc import get_lang


class ResPartner(models.Model):
    _inherit = 'res.partner'
    client_type_id = fields.Many2one('client.type', "Sector Type")
    industry_type_id = fields.Many2one('industry.type', "Industry Type")
    sigmentation_type_id = fields.Many2one('sigment.type', " Market Segment")
    lead_type_id = fields.Many2one('lead.type', "Lead / Opp")
    is_government = fields.Boolean("Is Government", default=False, related='client_type_id.is_government')
    government_cr = fields.Char("Government CR", required=False)
    is_employee = fields.Boolean("Is Employee", default=False)
    is_vendor = fields.Boolean("Is Vendor", compute='compute_is_vendor')
    is_a_partner = fields.Boolean()
    
    @api.depends('is_employee')
    def compute_is_vendor(self):
        for rec in self:
            if rec.is_employee == True:
                rec.is_vendor = False
            else:
                rec.is_vendor = True
#
#
# class AccountMoveInherit(models.Model):
#     _inherit = 'account.move'
#     is_employee = fields.Boolean("Type And Employee", relared='partner_id.is_employee')
#     is_vendor = fields.Boolean("vendor", relared='partner_id.is_vendor')
#
#     @api.onchange('partner_id', 'move_type')
#     def onchange_product_list(self):
#         if self.move_type == 'in_invoice':
#             return {'domain': {'partner_id': [('is_employee', '=', False), ('supplier_rank', '>', 0)]}}
#         if self.move_type == 'in_refund':
#             return {'domain': {'partner_id': [('is_employee', '=', False), ('supplier_rank', '>', 0)]}}
#             # return {'domain': {'partner_id': [('supplier_rank', '>', 0)]}}
#         if self.move_type == 'out_invoice':
#             return {'domain': {'partner_id': [('is_employee', '=', False), ('customer_rank', '>', 0)]}}
#             # return {'domain': {'partner_id': [('customer_rank', '>', 0), ('is_employee', '!=', True)]}}
#         if self.move_type == 'out_refund':
#             return {'domain': {'partner_id': [('customer_rank', '>', 0), ('is_employee', '=', False)]}}
#             # return {'domain': {'partner_id': [('supplier_rank', '>', 0),('is_employee', '!=', True)]}}
