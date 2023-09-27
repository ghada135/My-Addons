# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields


class SprintBacklogLine(models.Model):
    _name = 'sprint.backlog.bugs'
    _rec_name = 'task_id'
    sequence = fields.Integer(default=1)
    active = fields.Boolean(default=True)
    backlog_sprint_id = fields.Many2one('sprint.backlog')
    task_ids = fields.Many2many('project.task', related='backlog_sprint_id.task_bug_ids')
    task_line_bugs_ids = fields.Many2many('project.task','task_line_bugs_rel','task_bugs_rel', related='backlog_sprint_id.task_line_bugs_ids')
    task_bugs_ids = fields.Many2many('project.task','task_line_bugs_rel2','task_bugs_rel2',related='backlog_sprint_id.task_bugs_ids')



    task_id = fields.Many2one('project.task',domain="[('id','not in',task_bugs_ids),('id','not in',task_line_bugs_ids),('id','in',task_ids)]")
    project_id = fields.Many2one('project.project',
                                 related='task_id.project_id', store=1)

    developer_id = fields.Many2one('res.users', "Assigned Developer"
                                   , related='task_id.developer_id', store=1, readonly=0)

    user_id = fields.Many2one('res.users', "Assigned To"
                              , related='task_id.user_id', store=1)
    hours = fields.Float("Hours Spent", related='task_id.timesheet_ids.unit_amount')
    notes = fields.Text("Note")
    task_weight = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
        ('d', 'D'),
    ], required=0,
        string='Task Weight', related='task_id.task_weight', readonly=False,store=1)
    status = fields.Selection([
        ('to_do', 'To Do'),
        ('done', 'Done'),
        ('pending', 'Pending'),
    ],string='Status', required=0, default='to_do',
    )

    @api.depends('stage_id')
    @api.onchange('stage_id')
    def compute_status_task(self):
        for line in self:
            if line.stage_id.sprint_status_to_do == True:
                line.status = 'to_do'
            elif line.stage_id.sprint_status_pending == True:
                line.status = 'pending'
            elif line.stage_id.sprint_status_done == True:
                line.status = 'done'
            else:
                line.status = 'to_do'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('running', 'Running'),
        ('email_sent', 'Email Sent'),
        ('closed', 'Closed'),
    ], related='backlog_sprint_id.state',
        string='Status')
    stage_id = fields.Many2one('project.task.type', string='Stage',
                               related='task_id.stage_id', store=1
                               )


    approval_status = fields.Selection([
        ('approved', 'Approved'),
        ('refused', 'Refused'),
        ('not_assigned', 'Not Assigned To Developer'),
    ], string='Approved/Refused', default='approved')

    tag_ids = fields.Many2many('project.tags', string='Tags', oldname='categ_ids',related='task_id.tag_ids')

    is_done = fields.Boolean(compute='_compute_done')
    migration = fields.Selection([
        ('migrated', 'Migrated'),
        ('new', 'New'),
    ], string='Migration', default='new', readonly=1)

    def _compute_done(self):
        for rec in self:
            if rec.status == 'done':
                rec.is_done = True
            else:
                rec.is_done = False

    def migrate_yes(self):
        return {
            'name': ('Select Sprint'),
            'view_mode': 'form',
            'res_model': 'select.sprint',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_type': 'from_line',
                'default_is_bug': True,
                'default_backlog_sprint_bug_id': self.id,
                'default_sprint_name_id': self.backlog_sprint_id.id
            }, }

    def write(self, vals):
        """ Override write """
        for rec in self:
            approval_status_before = rec.approval_status
            task_before = rec.task_id
            status_before = rec.status
            notes_before = rec.notes
            res = super(SprintBacklogLine, self).write(vals)
            rec.onchange_backlog_sprint_ids(status_before, notes_before, task_before, approval_status_before)
            return res

    """ Method used to call values
     before and after changing """

    def onchange_backlog_sprint_ids(self, status_before, notes_before, task_before, approval_status_before):
        status_selection = dict(self.fields_get()['status']['selection'])
        approval_selection = dict(self.fields_get()['approval_status']['selection'])
        body = ''
        for line in self:
            if line.task_id:
                body += (task_before.name)
            if line.task_id != task_before:
                body += "<div>%s &#8594 %s </div>" % (task_before.name, self.task_id.name)
            if line.status != status_before:
                body += "<div>%s &#8594 %s </div>" % (
                    status_selection.get(status_before), (status_selection.get(self.status)))
            if line.notes != notes_before:
                body += "<div>%s &#8594 %s </div>" % (notes_before, self.notes)
            if line.approval_status != approval_status_before:
                body += "<div>%s &#8594 %s </div>" % (
                    approval_selection.get(approval_status_before), (approval_selection.get(self.approval_status)))
            line.backlog_sprint_id.message_post(body=body)


