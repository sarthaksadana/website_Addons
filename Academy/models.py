from odoo import models, fields, api

class Teachers(models.Model):
    _name = 'academy.teachers'

    name = fields.Char()
    biography = fields.Html()
    course_ids = fields.One2many('product.template', 'teacher_id', string="Courses")


class Courses(models.Model):
    _name = 'academy.courses'
    # _inherit = 'product.template'

    name = fields.Char()
    teacher_id = fields.Many2one('academy.teachers', string="Teacher")

class product_template(models.Model):
    _inherit='product.template'
    

    teacher_id = fields.Many2one('academy.teachers', string="Teacher")
