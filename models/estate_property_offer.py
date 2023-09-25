from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import date, timedelta, datetime
from dateutil import relativedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    _sql_constraints = [
        (
            'offer_price_greater_than_zero',
            'CHECK(price > 0)',
            'Offer price Must be greater than 0'
        )
    ]
    price = fields.Float()

    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)

    partner_id = fields.Many2one(comodel_name="res.partner", required=True)

    property_id = fields.Many2one(
        comodel_name="estate.property", required=True)

    validity = fields.Integer(default=7)

    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + \
                    relativedelta.relativedelta(days=record.validity)
            else:
                record.date_deadline = date.today() + relativedelta.relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                day1 = datetime(year=record.date_deadline.year,
                                month=record.date_deadline.month, day=record.date_deadline.day)
                day2 = datetime(year=record.create_date.year,
                                month=record.create_date.month, day=record.create_date.day)
                record.validity = (day1-day2).days
            else:
                today = date.today()
                day1 = datetime(year=record.date_deadline.year,
                                month=record.date_deadline.month, day=record.date_deadline.day)
                day2 = datetime(year=today.year,
                                month=today.month, day=today.day)
                record.validity = (day1-day2).days

    def action_refuse_offer(self):
        self.status = 'refused'
        return

    def action_accept_offer(self):
        self.status = 'accepted'
        self.property_id.state = "offer accepted"
        self.property_id.selling_price = self.price
        self.property_id.partner_id = self.partner_id

    @api.constrains('status')
    def _check_price(self):
        for record in self:
            if record.status == 'accepted':
                if (record.price/record.property_id.expected_price)*100 <= 90:
                    raise ValidationError(
                        "Price Offer must be at least > 90'%' of expected price")
