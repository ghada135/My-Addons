from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.osv import expression
from odoo.tools import float_is_zero, html_keep_url, is_html_empty


class SaleOrderInherit(models.Model):
    _inherit = "sale.order"
    # _name = "purchase.order"
    reference = fields.Char("Lead/Opp No",readonly=True)

    @api.onchange('partner_id')
    def onchange_product_list(self):
        return {'domain': {'partner_id': [('is_employee', '=', False), ('customer_rank', '>', 0)]}}
