from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'

    _rec_name = 'name'
    _order = 'name ASC'

    _sql_constraints = [
        (
            'constraint_uniq_name',
            'UNIQUE(name)',
            'Tag name must be unique'
        ),
    ]
    
    name = fields.Char(
        string='Property tag',
        required=True,
        copy=False
    )
    
    color = fields.Integer()
    
    

    
