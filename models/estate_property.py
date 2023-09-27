from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import date



class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    _inherit = ["mail.thread", "mail.activity.mixin"]

    _rec_name = 'name'
    _order = 'id desc'

    _sql_constraints = [
        (
            'expected_price_greater_than_zero',
            'CHECK(expected_price > 0)',
            'Expected price Must be greater than 0'
        ),
        (
            'selling_price_greater_than_zero',
            'CHECK(selling_price > 0)',
            'Selling price Must be greater than 0'
        ),
    ]

    active = fields.Boolean(default=True, invisible=True)

    name = fields.Char(string='Title', required=True, copy=False, index=True)

    description = fields.Text()

    property_type_id = fields.Many2one(
        comodel_name="estate.property.type", string="Property type")

    user_id = fields.Many2one(comodel_name="res.users", string="Salesman")

    partner_id = fields.Many2one(comodel_name="res.partner", string="Buyer")

    tags_ids = fields.Many2many(
        comodel_name="estate.property.tag", string="Tags")

    postcode = fields.Char()

    # The default availability date should be in 3 months
    date_availability = fields.Date(copy=False, default=lambda self: fields.date(
        date.today().year, date.today().month + 3, date.today().day))

    expected_price = fields.Float(required=True)

    selling_price = fields.Float(readonly=True, copy=False)

    bedrooms = fields.Integer(default=2)

    living_area = fields.Integer(string="Living area (m)")

    facades = fields.Integer()

    garage = fields.Boolean()

    garden = fields.Boolean()

    garden_area = fields.Integer()

    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])

    state = fields.Selection(selection=[('canceled', 'Canceled'), ('new', 'New'), ('offer received', 'Offer Received'),
                                        ('offer accepted', 'Offer Accepted'), ('sold', 'Sold')],
                             default='new', required=True, copy=False)

    offer_ids = fields.One2many(
        comodel_name="estate.property.offer", inverse_name="property_id")

    total_area = fields.Integer(
        compute="_compute_total_area", string="Total area (m)")

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    best_price = fields.Float(
        compute="_compute_best_price", string="Best offer")

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        best = 0
        for record in self:
            for offer in record.offer_ids:
                if offer.price > best:
                    best = offer.price
            record.best_price = best

    @api.onchange('garden')
    def onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None
        # return {'warning': {
        #         'title': _("Warning"),
        #         'message': ('This option is not supported for Authorize.net')}}

    def action_property_sold(self):
        self.state = "sold"
        return

    def action_property_cancel(self):
        self.state = "canceled"
        return

    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_no_new_canceled(self):
        for record in self:
            if record.state =='new' or record.state == 'canceled':
                pass
            else:
                raise ValidationError("Only new and canceled properties can be deleted") 