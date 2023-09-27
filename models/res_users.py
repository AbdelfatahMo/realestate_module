from odoo import fields, models



class ResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many("res.users","user_id", domain="[('state', 'in', ('new','offer','received'))]")

    

