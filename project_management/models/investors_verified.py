""" Initialize Hr Employee """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class InvestorVerified(models.Model):
    _name = 'investor.verified'
    name = fields.Char('Investor Name',related='partner_id.name')
    investor_number_id = fields.Char('Investor ID')
    bank_account_number = fields.Many2one(
        'res.partner.bank', 'Bank Account Number')
    partner_id = fields.Many2one('res.partner')
    payment_id = fields.Many2one('account.payment', string='Payment',)

    def open_payment(self):
        payment = self.env['account.payment'].search([('id', '=', self.payment_id.id)])
        if payment:
            return {
                'name': 'Payments',
                'type': 'ir.actions.act_window',
                'res_model': 'account.payment',
                'view_mode': 'tree,form',
                'view_type': 'form',
                'domain': [('id', 'in', payment.ids)],
                'target': 'current',
            }

    state = fields.Selection(
        [('new', 'New'),
         ('waiting_verification', 'Waiting Verification'),
         ('verified', 'Verified')],
        default='new')
    reference = fields.Char(string='Reference', readonly=True)
    @api.model
    def create(self, vals):
        res = super(InvestorVerified, self).create(vals)
        if not res.reference or res.reference == _('New'):
            res.reference = self.env['ir.sequence'].next_by_code('investor.verified') or _('New')
        return res
