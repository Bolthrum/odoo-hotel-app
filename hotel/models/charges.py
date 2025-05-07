# -*- coding: utf-8 -*-

# charges.py

from odoo import models, fields, api

class Charges(models.Model):
    _name = 'hotel.charges'
    _description = 'hotel charges master list'

    name = fields.Char("Item/Service")
    description = fields.Float("Price", digits=(10,2))


