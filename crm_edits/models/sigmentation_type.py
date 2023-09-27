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


class SigmentationType(models.Model):
    _name = "sigment.type"
    _rec_name = "sigment_name"
    sigment_name = fields.Char("Segmentation Type",required=True)
    sigment_id = fields.Char(string="Sigment ID")


