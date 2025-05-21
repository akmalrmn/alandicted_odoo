# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from datetime import datetime

class InventorySupply(models.Model):
    _name = 'alandicted.inventory.supply'
    _description = 'Inventory Supply'
    _order = 'date desc'

    name = fields.Char('Supply ID', readonly=True)
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
    
    @api.model
    def create(self, vals):
        """Override create method to generate supply ID that reuses deleted IDs"""
        if not vals.get('name'):
            # Get all existing supply IDs
            existing_ids = self.search([]).mapped('name')
            numeric_ids = []
            
            # Extract numeric parts from existing IDs
            for id_str in existing_ids:
                if id_str.startswith('#'):
                    try:
                        numeric_ids.append(int(id_str[1:]))
                    except ValueError:
                        continue
            
            # Find the next available ID (either first gap or max+1)
            next_id = 1
            if numeric_ids:
                numeric_ids.sort()
                # Find first gap in sequence
                for i, num in enumerate(numeric_ids, 1):
                    if i < num:
                        next_id = i
                        break
                else:
                    # If no gaps found, use max+1
                    next_id = max(numeric_ids) + 1
            
            vals['name'] = f'#{next_id:04d}'
            
        return super(InventorySupply, self).create(vals)
    
    def get_stock_level_status(self):
        """Returns the stock level status based on current and original stock"""
        if not self.original_stock:
            return 'normal'
        
        stock_percentage = (self.current_stock / self.original_stock) * 100
        
        if stock_percentage <= 10:
            return 'critical'
        elif stock_percentage <= 30:
            return 'warning'
        else:
            return 'normal' 