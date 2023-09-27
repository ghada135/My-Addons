# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields


class SprintBacklog(models.Model):
    _name = 'sprint.backlog'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'description'

    def onchange_backlog_sprint_ids(self):
        vals = []
        if self.backlog_sprint_ids:
            for line in self.backlog_sprint_ids:
                for task in line.task_id:
                    task.sprint_id = [(4, line.backlog_sprint_id.id)]

    task_ids = fields.Many2many('project.task')
    task_lines_ids = fields.Many2many('project.task','task_line_rel','lines_task_id_rel',compute='compute_tasks_liness')
    task_bug_ids = fields.Many2many('project.task','task_bug_rel','bugs_task__idrel',compute='compute_tasks_bugs')
    task_line_bugs_ids = fields.Many2many('project.task','task_bug','bugs_task_rel',compute='compute_tasks_lines_bugs')
    task_bugs_ids = fields.Many2many('project.task','task_line_bugs_rel2','task_bugs_rel2',compute='compute_all_task_bugs')

    def compute_all_task_bugs(self):
        all_task_bugs = self.env['sprint.backlog.bugs'].search([])
        if all_task_bugs:
            for line in all_task_bugs:
                self.task_bugs_ids =  [(4, line.task_id.id)]

    def compute_tasks_bugs(self):
        tasks_bug = self.env['project.task'].search([('tag_ids.is_bug', '=',True)])
        if tasks_bug:
            self.task_bug_ids = tasks_bug
        else:
            self.task_bug_ids = False

    def compute_tasks_lines_bugs(self):
        for rec in self:
            if rec.backlog_sprint_bugs_ids:
                for line in rec.backlog_sprint_bugs_ids:
                    rec.task_line_bugs_ids =  [(4, line.task_id.id)]

    def compute_tasks_liness(self):
        for rec in self:
            if rec.backlog_sprint_ids:
                for line in rec.backlog_sprint_ids:
                    rec.task_lines_ids =  [(4, line.task_id.id)]


    @api.onchange('backlog_sprint_ids')
    def compute_task_ids(self):
        for rec in self:
            if rec.backlog_sprint_ids:
                rec.task_ids = rec.backlog_sprint_ids.mapped('task_id')
            else:
                rec.task_ids = False

    def compute_project_ids(self):
        for rec in self:
            if rec.backlog_sprint_ids:
                projects = rec.backlog_sprint_ids.mapped('project_id')
                rec.project_progress_ids.unlink()
                for line in projects:
                    rec.project_progress_ids.create({
                            'project_id': line.id,
                            'backlog_sprint_id': rec.id,})

    @api.model
    def create(self, vals):
        """ Override Create """
        res = super(SprintBacklog, self).create(vals)
        res.onchange_backlog_sprint_ids()
        res.compute_project_ids()
        return res

    def write(self, vals):
        """ Override write """
        res = super(SprintBacklog, self).write(vals)
        self.onchange_backlog_sprint_ids()
        self.compute_project_ids()
        return res

    def compute_name(self):
        for rec in self:
            rec.description = str(rec.start_date) + '/' + str(rec.end_date)

    description = fields.Char(string="Description", compute='compute_name', tracking=True)
    start_date = fields.Date(string='Start date', required=True,
                             tracking=True)
    end_date = fields.Date(string='End date', required=True, tracking=True
                           )
    sprint_progress = fields.Integer(string='Sprint Progress', compute='compute_progress', tracking=True)
    sprint_bug_progress = fields.Integer(string='Sprint Bug Progress', compute='compute_bug_progress', tracking=True)

    def compute_progress(self):
        for rec in self:
            entry_len = self.env['sprint.backlog.line'].search_count([('approval_status', '=', 'approved'),
                                                                      ('status', '=', 'done'),
                                                                      ('backlog_sprint_id', '=', rec.id)])
            print('entry_len',entry_len)
            total_len = self.env['sprint.backlog.line'].search_count([('approval_status', '=', 'approved'),
                                                                      ('backlog_sprint_id', '=', rec.id)])
            print('total_len',total_len)
            if total_len != 0:
                rec.sprint_progress = (entry_len * 100) / total_len
            else:
                rec.sprint_progress = 0


    def compute_bug_progress(self):
        for rec in self:
            entry_len = self.env['sprint.backlog.bugs'].search_count([('approval_status', '=', 'approved'),
                                                                      ('status', '=', 'done'),
                                                                      ('backlog_sprint_id', '=', rec.id)])

            total_len = self.env['sprint.backlog.bugs'].search_count([('approval_status', '=', 'approved'),
                                                                      ('backlog_sprint_id', '=', rec.id)])
            if total_len != 0:
                rec.sprint_bug_progress = (entry_len * 100) / total_len
            else:
                rec.sprint_bug_progress = 0

    backlog_sprint_ids = fields.One2many('sprint.backlog.line', 'backlog_sprint_id')
    backlog_sprint_bugs_ids = fields.One2many('sprint.backlog.bugs', 'backlog_sprint_id')

    project_progress_ids = fields.One2many('project.progress', 'backlog_sprint_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('running', 'Running'),
        ('email_sent', 'Email Sent'),
        ('closed', 'Closed'),
    ], default='draft',
        string='Status', tracking=True)

    def start_spring(self):
        self.state = 'running'

    def reset_draft(self):
        self.state = 'draft'

    def close_spring(self):
        return {
            'name': ('Close Sprint'),
            'view_mode': 'form',
            'res_model': 'close.sprint',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'default_sprint_name_id': self.id}}

    def compute_status(self):
        for line in self.backlog_sprint_ids:
            if line.stage_id.sprint_status_to_do == True:
                line.status = 'to_do'
            elif line.stage_id.sprint_status_pending == True:
                line.status = 'pending'
            elif line.stage_id.sprint_status_done == True:
                line.status = 'done'
            else:
                line.status = 'to_do'

    def compute_status_bugs(self):
        for line in self.backlog_sprint_bugs_ids:
            if line.stage_id.sprint_status_to_do == True:
                line.status = 'to_do'
            elif line.stage_id.sprint_status_pending == True:
                line.status = 'pending'
            elif line.stage_id.sprint_status_done == True:
                line.status = 'done'
            else:
                line.status = 'to_do'

    def send_by_mail(self):
        email_from = self.env.user.email
        template = self.env.ref('sprint_backlog.approval_request')
        for rec in self.backlog_sprint_ids:
            if rec.developer_id.email:
                template.send_mail(self.id, force_send=True,
                                   email_values={
                                       'email_to': rec.developer_id.email,
                                       'email_from': email_from,
                                       'subject': 'your Task ',
                                       'body_html':
                                           """
                                           <div>
                                           Dear %s <br>\nYou have been assigned to the Task %s <br>\n
                                           </div><br>\n
                                           <div style="margin: 15px;">
                                            <a href="/web#view_type=form&amp;id=%s&amp;model=project.task" target="_blank"
                                               style="padding: 5px 10px; color: #FFFFFF; text-decoration: none; background-color: #875A7B; border: 1px solid #875A7B; border-radius: 3px">View Your Planning</a>
                                           </div>
        
                                     </div>
                                     """
                                           % (rec.developer_id.name,
                                              rec.task_id.name,
                                              rec.task_id.id,
                                              )},
                                   notif_layout='mail.mail_notification_light')
        self.state = 'email_sent'
