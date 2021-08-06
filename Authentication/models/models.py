from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit="res.users"

    auth_token=fields.Char()