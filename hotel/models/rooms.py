# -*- coding: utf-8 -*-

# rooms.py

from odoo import models, fields

class rooms(models.Model):
    _name = 'hotel.rooms'
    _description = 'hotel rooms master list'
    _order="name"


    name = fields.Char("Room No.")
    description = fields.Char("Room Description")
    
    roomtype_id = fields.Many2one('hotel.room_types', string="Room Type")
    roomtypename=fields.Char("Room Type",related='roomtype_id.name')
    
