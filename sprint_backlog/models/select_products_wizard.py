# -*- coding: utf-8 -*-
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class SelectProducts(models.TransientModel):
    _name = 'select.products'
    _description = 'Select Products'

    task_ids = fields.Many2many('project.task', string='Tasks', )
    # domain="[('id','not in',task_bugs_ids),('id','not in',sprint_task_ids)]")
    sprint_id = fields.Many2one('sprint.backlog')
    sprint_task_ids = fields.Many2many('project.task',
                                       'sprints_tasks_rel', related='sprint_id.task_ids',
                                       string='Tasks')
    task_bugs_ids = fields.Many2many('project.task', 'sprints_tasks_rel2', related='sprint_id.task_bugs_ids',
                                     string='Tasks')
    flag_order = fields.Char('Flag Order')

    def select_products(self):
        if self.flag_order == 'task':
            order_id = self.env['sprint.backlog'].browse(self._context.get('active_id', False))
            for product in self.task_ids:
                if product in self.sprint_id.task_lines_ids:
                    raise ValidationError("'%s' Already Exist"%(product.name))
                else:
                    self.env['sprint.backlog.line'].create({
                        'task_id': product.id,
                        'backlog_sprint_id': order_id.id,
                    })
        if self.flag_order == 'bug':
            order_id = self.env['sprint.backlog'].browse(self._context.get('active_id', False))
            for product in self.task_ids:
                if product in self.sprint_id.task_line_bugs_ids:
                    raise ValidationError("'%s' Already Exist"%(product.name))
                else:
                    self.env['sprint.backlog.bugs'].create({
                    'task_id': product.id,
                    'backlog_sprint_id': order_id.id,
                })
