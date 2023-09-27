""" Initialize Hr Employee """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class Investor(models.Model):
    _name = 'investor.investor'
    reference = fields.Char(string='Reference', readonly=True)
    name = fields.Char('Investor Name',related='partner_id.name')
    investor_number_id = fields.Char('Investor ID')
    bank_account_number = fields.Many2one(
        'res.partner.bank', 'Bank Account Number')
    partner_id = fields.Many2one('res.partner')
    state = fields.Selection(
        [('new', 'New'),
         ('waiting_verification', 'Waiting Verification'),
         ('verified', 'Verified')],
        default='new')
    journal_id = fields.Many2one('account.journal', string='Journal',)
    payment_id = fields.Many2one('account.payment', string='Payment',)

    @api.model
    def create(self, vals):
        res = super(Investor, self).create(vals)
        if not res.reference or res.reference == _('New'):
            res.reference = self.env['ir.sequence'].next_by_code('investor.investor') or _('New')
        return res

    def waiting_verification(self):
        for rec in self:
            rec.state= 'waiting_verification'

    def create_payment(self):
        for rec in self:
            payment = self.env['account.payment'].create([{
                'payment_type': 'inbound',
                # 'partner_type': 'supplier',
                'partner_id': rec.partner_id.id,
                'journal_id': rec.journal_id.id,
                'ref': 'investor',
                'date': fields.Date.today(),

            }])
            rec.payment_id = payment


    def open_payment(self):
        payment = self.env['account.payment'].search([('id','=',self.payment_id.id)])
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




    def verified(self):
        for rec in self:
            rec.state= 'verified'
            self.env['investor.verified'].create([{
                'name': rec.name,
                'investor_number_id': rec.investor_number_id,
                'bank_account_number': rec.bank_account_number.id,
                'partner_id': rec.partner_id.id,
                'state': rec.state,
                'payment_id': rec.payment_id.id,
            }])




