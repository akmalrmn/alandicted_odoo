# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from datetime import datetime

class Project(models.Model):
    _name = 'alandicted.project'
    _description = 'Project'
    _order = 'date desc'

    name = fields.Char('Project ID', default=lambda self: self.env['ir.sequence'].next_by_code('alandicted.project') or '#0000')
    date = fields.Date('Date', default=fields.Date.today)
    buyer = fields.Char('Buyer', required=True)
    destination = fields.Char('Destination', required=True)
    item_id = fields.Many2one('alandicted.inventory.supply', string='Item', domain=[('status', '=', 'completed')])
    quantity = fields.Integer('Quantity', default=1)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('inprogress', 'In Progress'),
        ('completed', 'Completed'),
    ], string='Route Status', default='pending')
    
    @api.model
    def create(self, vals):
        # If the project is being created, check if we need to update inventory
        if vals.get('item_id') and vals.get('quantity'):
            inventory_item = self.env['alandicted.inventory.supply'].browse(vals['item_id'])
            if inventory_item.current_stock >= vals['quantity']:
                # Decrement inventory stock
                inventory_item.write({
                    'current_stock': inventory_item.current_stock - vals['quantity']
                })
            else:
                # Not enough stock, adjust quantity to available stock
                vals['quantity'] = inventory_item.current_stock
                inventory_item.write({
                    'current_stock': 0
                })
        
        return super(Project, self).create(vals) 