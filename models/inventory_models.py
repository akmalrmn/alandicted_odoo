# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from datetime import datetime

class InventorySupply(models.Model):
    _name = 'alandicted.inventory.supply'
    _description = 'Inventory Supply'
    _order = 'date desc'

    name = fields.Char('Supply ID', default=lambda self: self.env['ir.sequence'].next_by_code('alandicted.inventory.supply') or '#000')
    date = fields.Date('Date', default=fields.Date.today)
    supplier = fields.Char('Supplier', required=True)
    category = fields.Char('Category', required=True)
    storage_location = fields.Char('Storage Location', required=True)
    items = fields.Integer('Items', default=1)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ], string='Status', default='pending')
    original_stock = fields.Integer('Original Stock', default=0)
    current_stock = fields.Integer('Current Stock', default=0)
    
    def get_stock_level_status(self):
        if not self.original_stock:
            return 'normal'
        
        stock_percentage = (self.current_stock / self.original_stock) * 100
        
        if stock_percentage <= 10:
            return 'critical'
        elif stock_percentage <= 30:
            return 'warning'
        else:
            return 'normal' 