# -*- coding: utf-8 -*-

# roomTypes.py

from odoo import models, fields

class roomTypes(models.Model):
    _name = 'hotel.room_types'
    _description = 'hotel roomTypes master list'
    _order="name"

    name = fields.Char("Room Type")
    description = fields.Char("Room Type Description")
    imageroom = fields.Image("Room")
    imagebathroom  = fields.Image("Bath Room")
    
    dailycharges_ids=fields.One2many('hotel.dailycharges','roomtype_id', string='Daily Charges')
    room_ids=fields.One2many('hotel.rooms','roomtype_id', string='Rooms')
    
        
class dailycharges(models.Model):
    _name = 'hotel.dailycharges'
    _description = 'hotel roomtype daily charges list'
    
    charge_id = fields.Many2one('hotel.charges',string="Charge Title")
    amount = fields.Float("Daily Amount", digits=(10,2))
    roomtype_id = fields.Many2one('hotel.room_types', string="Room Type")   

