# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError


class ProjectTask(models.Model):
    _inherit = 'project.task'
    sprint_id = fields.Many2many('sprint.backlog',
                                 'sprint_task_rel',
                                 )
    developer_id = fields.Many2one('res.users', "Assigned Developer",
                                   domain="[('is_developer','=',True)]")
    task_weight = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
        ('d', 'D'),
    ], required=0,
        string='Task Weight')

    sprinted = fields.Boolean('Added To Sprint')
    is_bug = fields.Boolean('IS Bug Tag',compute='compute_is_bug')
    def compute_is_bug(self):
        for rec in self.tag_ids:
            if rec.is_bug == True:
                self.is_bug = True
            else:
                self.is_bug = False


    sprint_control = fields.Boolean(compute='compute_sprint_view')
    task_periority = fields.Char("Task Periority")

    def compute_sprint_view(self):
        if self.env.user.has_group('sprint_backlog.group_sprint') or self.env.user.has_group(
                'sprint_backlog.group_sprint_lines'):
            self.sprint_control = True
        else:
            self.sprint_control = False


    @api.onchange('developer_id')
    def onchange_developer_id(self):
        self.timesheet_ids = [(5,)]
        vals = []
        if self.developer_id.employee_ids:
            vals.append((0, 0, {
                'date': fields.Date.today(),
                'employee_id': self.developer_id.employee_ids[0].id,
                'name': '/',
                'project_id': self.project_id.id,
            }))
        self.timesheet_ids = vals


    def onchange_sprint_id(self):
        for sprint in self.sprint_id:
            print(sprint.description)
            sprint.backlog_sprint_ids.create({
                'task_id': self.id,
                'backlog_sprint_id': sprint.id,
                'status': 'to_do',
            })

    @api.model
    def create(self, vals):
        """ Override Create """
        res = super(ProjectTask, self).create(vals)
        res.onchange_sprint_id()
        return res

    def write(self, vals):
        """ Override write """
        res = super(ProjectTask, self).write(vals)
        tasks = self.env['sprint.backlog.line'].search([
            ('task_id', '=', self.id),
            ('backlog_sprint_id', 'in', self.sprint_id.ids)])
        if tasks:
            pass
        else:
            self.onchange_sprint_id()
            # self.onchange_backlog_sprint_ids()
        return res



