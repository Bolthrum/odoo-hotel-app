#Guest Registration Model

# -*- coding: utf-8 -*-

#guestregistration.py

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class guestregistration(models.Model):
    _name = 'hotel.guestregistration'
    _description = 'hotel guest registration list'

    # State field for workflow management
    state = fields.Selection([
        ('draft', 'Draft'),
        ('reserved', 'Reserved'),
        ('checkedin', 'Checked In'),
        ('checkedout', 'Checked Out'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', readonly=True, tracking=True)

    room_id = fields.Many2one("hotel.rooms", string="Room No.")
    guest_id = fields.Many2one("hotel.guests", string="Guest Name")

    #roomname <- related fields found in hotel.rooms    
    roomname = fields.Char("Room No.", related='room_id.name')

    #roomtname <- room type name found in hotel.rooms 
    #also related to hotel.roomtypes
    roomtname = fields.Char("Room Type", related='room_id.roomtypename')

    #guestname <- related field found as computed field called name 
    #in hotel.guests
    guestname = fields.Char("Guest Name", related='guest_id.name')

    datecreated = fields.Date("Date Created", default=lambda self: fields.Date.today())
    datefromSched = fields.Date("Scheduled Check In")
    datetoSched = fields.Date("Scheduled Check Out")
    datefromAct = fields.Date("Actual Check In")
    datetoAct = fields.Date("Actual Check Out")

    #computed field called name <- concatenation of room name and guest name
    name = fields.Char("Guest Registration", compute='_compute_name', store=False)
    
    @api.depends('room_id', 'guest_id')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.roomname}, {record.guestname}"

    # State change methods
    def action_reserve(self):
        for record in self:
            if not(record.guest_id):
                raise ValidationError('Please enter a valid guest.')
            elif not(record.roomname):
                raise ValidationError('Please enter a valid Room Number')
            elif not(record.datefromSched):
                raise ValidationError('Please enter a valid Date From Scheule')
            elif not(record.datetoSched):    
                raise ValidationError('Please enter a valid Date To Schedule.')          
            elif (record.datetoSched<record.datefromSched):    
                raise ValidationError('Invalid Date Range.')
            else:
                #get pk value of guest registration
                pkid = record.id
                #postgresql function check for conflicts
                self._cr.execute("select * from public.fncheck_registrationconflict("+str(pkid)+")")
                result = self._cr.fetchall()
                
                #query results
                result_cnt = result[0][0]
                result_msg = result[0][1]
                
                if (result_cnt==0):
                    record.state= "reserved"
                else:
                    raise ValidationError(result_msg)

    def action_checkin(self):
        for record in self:
            if not record.guest_id:
                raise ValidationError('Please enter a valid guest.')
            elif not record.room_id:
                raise ValidationError('Please enter a valid Room Number')
            elif not record.datefromSched or not record.datetoSched:
                raise ValidationError('Please enter valid dates')
            elif record.datetoSched < record.datefromSched:
                raise ValidationError('Invalid Date Range.')
            
            # Check for conflicts
            pkid = record.id
            self._cr.execute("select * from public.fncheck_registrationconflict("+str(pkid)+")")
            result = self._cr.fetchall()
            result_cnt = result[0][0]
            result_msg = result[0][1]
            
            if result_cnt == 0:
                record.state = "checkedin"  # Changed from "reserved"
                record.datefromAct = fields.Date.today()  # Set actual check-in date
            else:
                raise ValidationError(result_msg)

    def action_checkout(self):
        for record in self:
         if (record.state=="checkedin"):  
            record.state= "checkedout"
         else:                     
            raise ValidationError("Guest is not CHECKED IN.") 

    def action_cancel(self):
        for record in self:
         if (record.state=="checkedin"):  
            raise ValidationError("Guest has already CHECKED IN.")           
         else:                     
            record.state= "cancelled"