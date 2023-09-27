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

    offer_ids = fields.One2many(comodel_name="estate.property.offer", inverse_name="property_type_id")

    offer_count = offer_count = fields.Integer(compute='_compute_offer_count', string='Offer Count')
    
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(self.offer_ids)
