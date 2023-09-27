# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError


class ProjectTags(models.Model):
    _inherit = 'project.tags'
    is_bug = fields.Boolean('IS Bug Tag')
