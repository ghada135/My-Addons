# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'
    is_developer = fields.Boolean(string="Is Developer")



