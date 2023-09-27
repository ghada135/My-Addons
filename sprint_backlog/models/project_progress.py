# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields


class ProjectProgress(models.Model):
    _name = 'project.progress'
    backlog_sprint_id = fields.Many2one('sprint.backlog')
    project_id = fields.Many2one('project.project')
    num_of_tasks_approved = fields.Integer('Tasks Approved', compute='compute_tasks_approved')
    num_of_tasks_done = fields.Integer('Tasks Done', compute='compute_tasks_done')
    num_of_tasks_to_done = fields.Integer('Tasks To Done',compute='compute_progress')
    project_progress = fields.Integer(string='Project Progress', compute='compute_progress')
    description = fields.Char(string="Sprint Backlog", compute='compute_name')

    def compute_name(self):
        for rec in self:
            rec.description = rec.backlog_sprint_id.description

    def compute_tasks_approved(self):
        for rec in self:
            tasks_approved = self.env['sprint.backlog.line'].search([
                ('approval_status', '=', 'approved'),
                ('project_id', '=', rec.project_id.id),
                ('backlog_sprint_id', '=', rec.backlog_sprint_id.id)])
            if tasks_approved:
                rec.num_of_tasks_approved = len(tasks_approved)
            else:
                rec.num_of_tasks_approved = 0

    def compute_tasks_done(self):
        for rec in self:
            tasks_done = self.env['sprint.backlog.line'].search([
                ('status', '=', 'done'),
                ('approval_status', '=', 'approved'),
                ('project_id', '=', rec.project_id.id),
                ('backlog_sprint_id', '=', rec.backlog_sprint_id.id)])
            if tasks_done:
                rec.num_of_tasks_done = len(tasks_done)
            else:
                rec.num_of_tasks_done = 0

    def compute_progress(self):
        for rec in self:
            if rec.num_of_tasks_approved !=0:
                rec.num_of_tasks_to_done = rec.num_of_tasks_approved - rec.num_of_tasks_done
                rec.project_progress = (rec.num_of_tasks_done * 100) / rec.num_of_tasks_approved
                print(rec.project_progress)
            else:
                rec.project_progress = 0
                rec.num_of_tasks_to_done = 0

