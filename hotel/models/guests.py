# -*- coding: utf-8 -*-

# guests.py

from datetime import date
from odoo import models, fields, api

class guests(models.Model):
    _name = 'hotel.guests'
    _description = 'hotel guests master list'
    _order='lastname,firstname,middlename'
    
    # name
    lastname = fields.Char("Lastname")
    firstname = fields.Char("Firstname")
    middlename = fields.Char("Middlename")
    
    # address                  
    address_streetno  = fields.Char("Address/ Street & No.")       
    address_area  = fields.Char("Address / Area,Unit&Bldg,Brgy")                                                          
    address_city  = fields.Char("Address / City/Town" )
    address_province  = fields.Char("Address / Province/State" )
    zipcode = fields.Char("ZIP Code" )
    
    # pesronals
    contactno = fields.Char("Contact No.")
    email = fields.Char("Email")
    gender = fields.Selection([('FEMALE','Female'),('MALE','Male')],string="Gender")
    birthdate = fields.Date("BirthDate")
    photo = fields.Image("Guest Photo")  
    
    #################################################################################### 
    
    # functions    
    @api.depends('birthdate')
    def _compute_age(self):
        today = date.today()
        for rec in self:
            if rec.birthdate:
                rec.age = today.year - rec.birthdate.year - (
                    (today.month, today.day) < (rec.birthdate.month, rec.birthdate.day)
                )
            else:
                rec.age = 0
    
    @api.depends('lastname','firstname','middlename')
    def _compute_name(self):
        for rec in self:
              rec.name=f"{rec.lastname}, {rec.firstname} {rec.middlename}"
    
    # computeed fields
    name = fields.Char(string='Guest Name', compute='_compute_name')
    age = fields.Integer(string="Age", compute="_compute_age", store=True)
