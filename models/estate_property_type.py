from odoo import fields, api, models, _


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'

    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Property type',
        required=True,
        copy=False
    )
    
    sequence=fields.Integer(string='Sequence',default=1,help="Used to order Types.")

    property_ids = fields.One2many(
        comodel_name="estate.property", inverse_name="property_type_id")
