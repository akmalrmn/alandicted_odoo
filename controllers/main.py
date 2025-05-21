# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
import base64
import io
import xlsxwriter
import json

class AlandictedController(http.Controller):

    @http.route('/alandicted', type='http', auth='user', website=True)
    def index(self, **kwargs):
        # Simple HTML response without a template
        return """
        <html>
            <head>
                <title>Alandicted - Test Page</title>
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
                <style>
                    body { font-family: 'Roboto', sans-serif; padding: 20px; }
                    .card { margin-bottom: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
                    .card-header { font-weight: bold; }
                    .btn-custom { margin-right: 10px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="jumbotron">
                        <h1>Alandicted ERP System</h1>
                        <p>Welcome to the Alandicted ERP System. Select a module to begin:</p>
                    </div>

                    <div class="row">
                        <div class="col-md-4">
                            <div class="card">
                                <div class="card-header bg-primary text-white">Dashboard</div>
                                <div class="card-body">
                                    <p>Get an overview of your business metrics and important information.</p>
                                    <a href="/alandicted/dashboard" class="btn btn-primary">Go to Dashboard</a>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="card">
                                <div class="card-header bg-success text-white">Inventory</div>
                                <div class="card-body">
                                    <p>Track stock levels, manage warehouses, and optimize your inventory processes.</p>
                                    <a href="/alandicted/inventory" class="btn btn-success">Go to Inventory</a>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="card">
                                <div class="card-header bg-danger text-white">Projects</div>
                                <div class="card-body">
                                    <p>Plan, execute, and monitor your projects with ease.</p>
                                    <a href="/alandicted/project" class="btn btn-danger">Go to Projects</a>
                                </div>
                            </div>
                        </div>
                    </div>

                    <hr>
                    <footer class="text-center">
                        <p>&copy; 2025 Alandicted ERP System</p>
                    </footer>
                </div>
                <script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js"></script>
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.bundle.min.js"></script>
            </body>
        </html>
        """

    @http.route('/alandicted/debug', type='http', auth='user', website=True)
    def debug(self, **kwargs):
        module = request.env['ir.module.module'].sudo().search([('name', '=', 'alandicted_odoo')], limit=1)
        templates = request.env['ir.ui.view'].sudo().search([('module', '=', 'alandicted_odoo')])

        template_list = "<ul>"
        for template in templates:
            template_list += f"<li>{template.name} (ID: {template.id}, XML ID: {template.xml_id})</li>"
        template_list += "</ul>"

        return f"""
        <html>
            <head>
                <title>Alandicted - Debug Info</title>
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
            </head>
            <body>
                <div class="container mt-5">
                    <h1>Module Debug Information</h1>
                    <div class="card mb-4">
                        <div class="card-header">Module Status</div>
                        <div class="card-body">
                            <p><strong>Name:</strong> {module.name if module else 'Not found'}</p>
                            <p><strong>State:</strong> {module.state if module else 'N/A'}</p>
                            <p><strong>Latest Version:</strong> {module.latest_version if module else 'N/A'}</p>
                        </div>
                    </div>

                    <div class="card">
                        <div class="card-header">Templates</div>
                        <div class="card-body">
                            <p><strong>Template Count:</strong> {len(templates)}</p>
                            {template_list}
                        </div>
                    </div>

                    <div class="mt-4">
                        <a href="/alandicted" class="btn btn-primary">Return to Home</a>
                        <a href="/alandicted/debug/template" class="btn btn-success">Test Debug Template</a>
                    </div>
                </div>
            </body>
        </html>
        """

    @http.route('/alandicted/debug/template', type='http', auth='user', website=True)
    def debug_template(self, **kwargs):
        try:
            return request.render('alandicted_odoo.debug_template', {})
        except Exception as e:
            return f"""
            <html>
                <head>
                    <title>Error</title>
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
                </head>
                <body>
                    <div class="container mt-5">
                        <div class="alert alert-danger">
                            <h4>Error loading debug template</h4>
                            <p>{str(e)}</p>
                        </div>
                        <a href="/alandicted" class="btn btn-primary">Return to Home</a>
                        <a href="/alandicted/debug" class="btn btn-secondary">Debug Information</a>
                    </div>
                </body>
            </html>
            """

    @http.route('/alandicted/dashboard', type='http', auth='user', website=True)
    def dashboard(self, **kwargs):
        try:
            return request.render('alandicted_odoo.dashboard_template', {})
        except Exception as e:
            return f"""
            <html>
                <head>
                    <title>Error</title>
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
                </head>
                <body>
                    <div class="container mt-5">
                        <div class="alert alert-danger">
                            <h4>Error loading dashboard template</h4>
                            <p>{str(e)}</p>
                        </div>
                        <a href="/alandicted" class="btn btn-primary">Return to Home</a>
                        <a href="/alandicted/debug" class="btn btn-secondary">Debug Information</a>
                    </div>
                </body>
            </html>
            """

    @http.route('/alandicted/inventory', type='http', auth='user', website=True)
    def inventory(self, **kwargs):
        try:
            start_date = kwargs.get('start_date', False)
            end_date = kwargs.get('end_date', False)
            status_filter = kwargs.get('status', False)
            category_filter = kwargs.get('category', False)

            domain = []
            if start_date and end_date:
                domain += [('date', '>=', start_date), ('date', '<=', end_date)]
            if status_filter:
                domain += [('status', '=', status_filter)]
            if category_filter:
                domain += [('category', '=', category_filter)]

            supplies = request.env['alandicted.inventory.supply'].search(domain, order='name')

            all_categories = request.env['alandicted.inventory.supply'].search([]).mapped('category')
            unique_categories = list(set(all_categories))

            inventory_items = []
            for supply in supplies:
                stock_status = supply.get_stock_level_status()
                inventory_items.append({
                    'id': supply.id,
                    'supply_id': supply.name,
                    'date': supply.date,
                    'supplier': supply.supplier,
                    'category': supply.category,
                    'storage_location': supply.storage_location,
                    'items': supply.items,
                    'status': supply.status,
                    'stock_status': stock_status,
                    'original_stock': supply.original_stock,
                    'current_stock': supply.current_stock,
                })

            template_vals = {
                'inventory_items': inventory_items,
                'start_date': start_date or '',
                'end_date': end_date or '',
                'status_filter': status_filter or '',
                'category_filter': category_filter or '',
                'categories': unique_categories
            }

            return request.render('alandicted_odoo.inventory_template', template_vals)
        except Exception as e:
            return f"""
            <html>
                <head>
                    <title>Error</title>
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
                </head>
                <body>
                    <div class="container mt-5">
                        <div class="alert alert-danger">
                            <h4>Error loading inventory template</h4>
                            <p>{str(e)}</p>
                        </div>
                        <a href="/alandicted" class="btn btn-primary">Return to Home</a>
                        <a href="/alandicted/debug" class="btn btn-secondary">Debug Information</a>
                    </div>
                </body>
            </html>
            """

    @http.route('/alandicted/inventory/add', type='http', auth='user', website=True)
    def add_supply(self, **kwargs):
        try:
            return request.render('alandicted_odoo.inventory_add_supply_template', {})
        except Exception as e:
            return f"""
            <html>
                <head>
                    <title>Error</title>
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
                </head>
                <body>
                    <div class="container mt-5">
                        <div class="alert alert-danger">
                            <h4>Error loading add supply template</h4>
                            <p>{str(e)}</p>
                        </div>
                        <a href="/alandicted/inventory" class="btn btn-primary">Return to Inventory</a>
                    </div>
                </body>
            </html>
            """

    @http.route('/alandicted/inventory/save', type='http', auth='user', website=True, methods=['POST'], csrf=False)
    def save_supply(self, **post):
        try:
            supply = request.env['alandicted.inventory.supply'].create({
                'supplier': post.get('supplier'),
                'category': post.get('category'),
                'storage_location': post.get('storage_location'),
                'items': int(post.get('items', 1)),
                'status': post.get('status', 'pending'),
                'original_stock': int(post.get('original_stock', 0)),
                'current_stock': int(post.get('current_stock', 0)),
            })

            return request.redirect('/alandicted/inventory')
        except Exception as e:
            return f"""
            <html>
                <head>
                    <title>Error</title>
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
                </head>
                <body>
                    <div class="container mt-5">
                        <div class="alert alert-danger">
                            <h4>Error saving supply</h4>
                            <p>{str(e)}</p>
                        </div>
                        <a href="/alandicted/inventory/add" class="btn btn-primary">Try Again</a>
                        <a href="/alandicted/inventory" class="btn btn-secondary">Return to Inventory</a>
                    </div>
                </body>
            </html>
            """

    @http.route('/alandicted/inventory/export', type='http', auth='user', website=True)
    def export_inventory(self, **kwargs):
        try:
            supplies = request.env['alandicted.inventory.supply'].search([])

            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output)
            worksheet = workbook.add_worksheet('Inventory')

            headers = ['Supply ID', 'Date', 'Supplier', 'Category', 'Storage Location',
                       'Items', 'Status', 'Original Stock', 'Current Stock', 'Stock Status']
            for col, header in enumerate(headers):
                worksheet.write(0, col, header)

            for row, supply in enumerate(supplies, start=1):
                stock_status = supply.get_stock_level_status()
                worksheet.write(row, 0, supply.name)
                worksheet.write(row, 1, supply.date.strftime('%Y-%m-%d') if supply.date else '')
                worksheet.write(row, 2, supply.supplier)
                worksheet.write(row, 3, supply.category)
                worksheet.write(row, 4, supply.storage_location)
                worksheet.write(row, 5, supply.items)
                worksheet.write(row, 6, dict(supply._fields['status'].selection).get(supply.status))
                worksheet.write(row, 7, supply.original_stock)
                worksheet.write(row, 8, supply.current_stock)
                worksheet.write(row, 9, stock_status)

            workbook.close()

            output.seek(0)
            data = output.read()
            b64_data = base64.b64encode(data)

            filename = 'inventory_export.xlsx'
            return request.make_response(
                data,
                headers=[
                    ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                    ('Content-Disposition', f'attachment; filename="{filename}"')
                ]
            )
        except Exception as e:
            return f"""
            <html>
                <head>
                    <title>Error</title>
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
                </head>
                <body>
                    <div class="container mt-5">
                        <div class="alert alert-danger">
                            <h4>Error exporting inventory</h4>
                            <p>{str(e)}</p>
                        </div>
                        <a href="/alandicted/inventory" class="btn btn-primary">Return to Inventory</a>
                    </div>
                </body>
            </html>
            """

    @http.route('/alandicted/project', type='http', auth='user', website=True)
    def project(self, **kwargs):
        try:
            return request.render('alandicted_odoo.project_template', {})
        except Exception as e:
            return f"""
            <html>
                <head>
                    <title>Error</title>
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
                </head>
                <body>
                    <div class="container mt-5">
                        <div class="alert alert-danger">
                            <h4>Error loading project template</h4>
                            <p>{str(e)}</p>
                        </div>
                        <a href="/alandicted" class="btn btn-primary">Return to Home</a>
                        <a href="/alandicted/debug" class="btn btn-secondary">Debug Information</a>
                    </div>
                </body>
            </html>
            """

    @http.route('/alandicted/inventory/delete/<int:supply_id>', type='http', auth='user', website=True)
    def delete_supply(self, supply_id, **kwargs):
        try:
            supply = request.env['alandicted.inventory.supply'].browse(supply_id)
            if supply:
                supply.unlink()

            return request.redirect('/alandicted/inventory')
        except Exception as e:
            return f"""
            <html>
                <head>
                    <title>Error</title>
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
                </head>
                <body>
                    <div class="container mt-5">
                        <div class="alert alert-danger">
                            <h4>Error deleting supply</h4>
                            <p>{str(e)}</p>
                        </div>
                        <a href="/alandicted/inventory" class="btn btn-primary">Return to Inventory</a>
                    </div>
                </body>
            </html>
            """

    @http.route('/alandicted/inventory/update_stock/<int:supply_id>/<int:quantity>', type='http', auth='user', website=True)
    def update_stock(self, supply_id, quantity, **kwargs):
        try:
            supply = request.env['alandicted.inventory.supply'].browse(supply_id)
            if supply:
                new_stock = supply.current_stock + quantity
                if new_stock < 0:
                    new_stock = 0
                supply.write({'current_stock': new_stock})

            return request.redirect('/alandicted/inventory')
        except Exception as e:
            return f"""
            <html>
                <head>
                    <title>Error</title>
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
                </head>
                <body>
                    <div class="container mt-5">
                        <div class="alert alert-danger">
                            <h4>Error updating stock</h4>
                            <p>{str(e)}</p>
                        </div>
                        <a href="/alandicted/inventory" class="btn btn-primary">Return to Inventory</a>
                    </div>
                </body>
            </html>
            """

    @http.route('/alandicted/inventory/change_status/<int:supply_id>/<string:status>', type='http', auth='user', website=True)
    def change_status(self, supply_id, status, **kwargs):
        try:
            supply = request.env['alandicted.inventory.supply'].browse(supply_id)
            if supply and status in ['completed', 'pending']:
                supply.write({'status': status})

            return request.redirect('/alandicted/inventory')
        except Exception as e:
            return f"""
            <html>
                <head>
                    <title>Error</title>
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
                </head>
                <body>
                    <div class="container mt-5">
                        <div class="alert alert-danger">
                            <h4>Error changing status</h4>
                            <p>{str(e)}</p>
                        </div>
                        <a href="/alandicted/inventory" class="btn btn-primary">Return to Inventory</a>
                    </div>
                </body>
            </html>
            """

    @http.route('/alandicted/project', type='http', auth='user', website=True)
    def project(self, **kwargs):
        try:
            domain = []

            # Apply date filter if provided
            if kwargs.get('start_date') and kwargs.get('end_date'):
                domain.append(('date', '>=', kwargs.get('start_date')))
                domain.append(('date', '<=', kwargs.get('end_date')))

            # Get projects from database
            projects_data = []
            projects = request.env['alandicted.project'].search(domain, order='date desc')

            for project in projects:
                item_name = project.item_id.category if project.item_id else ''

                projects_data.append({
                    'id': project.id,
                    'project_id': project.name,
                    'date': project.date.strftime('%m/%d/%Y') if project.date else '',
                    'buyer': project.buyer,
                    'item': item_name,
                    'quantity': project.quantity,
                    'destination': project.destination,
                    'status': project.status
                })

            return request.render('alandicted_odoo.project_template', {
                'projects': projects_data if projects_data else None,
                'start_date': kwargs.get('start_date', ''),
                'end_date': kwargs.get('end_date', '')
            })
        except Exception as e:
            return f"""
            <html>
                <head>
                    <title>Error</title>
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
                </head>
                <body>
                    <div class="container mt-5">
                        <div class="alert alert-danger">
                            <h4>Error loading project template</h4>
                            <p>{str(e)}</p>
                        </div>
                        <a href="/alandicted" class="btn btn-primary">Return to Home</a>
                        <a href="/alandicted/debug" class="btn btn-secondary">Debug Information</a>
                    </div>
                </body>
            </html>
            """

    @http.route('/alandicted/project/add', type='http', auth='user', website=True)
    def add_project(self, **kwargs):
        if request.httprequest.method == 'POST':
            try:
                # Create project in database
                project_vals = {
                    'buyer': kwargs.get('buyer', ''),
                    'destination': kwargs.get('destination', ''),
                    'quantity': int(kwargs.get('quantity', 0)),
                    'status': kwargs.get('status', 'pending'),
                }

                # Set date if provided
                if kwargs.get('date'):
                    project_vals['date'] = kwargs.get('date')

                # Set item_id if provided
                if kwargs.get('item_id'):
                    project_vals['item_id'] = int(kwargs.get('item_id'))

                # Create project
                request.env['alandicted.project'].sudo().create(project_vals)

                return request.redirect('/alandicted/project')
            except Exception as e:
                return f"""
                <html>
                    <head>
                        <title>Error</title>
                        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
                    </head>
                    <body>
                        <div class="container mt-5">
                            <div class="alert alert-danger">
                                <h4>Error creating project</h4>
                                <p>{str(e)}</p>
                            </div>
                            <a href="/alandicted/project/add" class="btn btn-primary">Try Again</a>
                            <a href="/alandicted/project" class="btn btn-secondary">Return to Projects</a>
                        </div>
                    </body>
                </html>
                """
        else:
            try:
                # Get completed inventory items for dropdown
                inventory_items = []
                supplies = request.env['alandicted.inventory.supply'].search([
                    ('status', '=', 'completed'),
                    ('current_stock', '>', 0)
                ])

                for supply in supplies:
                    inventory_items.append({
                        'id': supply.id,
                        'supply_id': supply.name,
                        'category': supply.category,
                        'current_stock': supply.current_stock
                    })

                return request.render('alandicted_odoo.add_project_template', {
                    'inventory_items': inventory_items
                })
            except Exception as e:
                return f"""
                <html>
                    <head>
                        <title>Error</title>
                        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
                    </head>
                    <body>
                        <div class="container mt-5">
                            <div class="alert alert-danger">
                                <h4>Error loading add project template</h4>
                                <p>{str(e)}</p>
                            </div>
                            <a href="/alandicted/project" class="btn btn-primary">Return to Projects</a>
                        </div>
                    </body>
                </html>
                """

    @http.route('/alandicted/project/export_excel', type='http', auth="user", website=True, methods=['GET'])
    def export_project_excel(self, **kwargs):
        try:
            # Get projects
            domain = []

            # Apply date filter if provided
            if kwargs.get('start_date') and kwargs.get('end_date'):
                domain.append(('date', '>=', kwargs.get('start_date')))
                domain.append(('date', '<=', kwargs.get('end_date')))

            projects = request.env['alandicted.project'].search(domain, order='date desc')

            if not projects:
                # No projects found, return a message
                return """
                <html>
                    <head>
                        <title>No Projects</title>
                        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
                    </head>
                    <body>
                        <div class="container mt-5">
                            <div class="alert alert-warning">
                                <h4>No Projects Found</h4>
                                <p>There are no projects available to export to Excel.</p>
                            </div>
                            <a href="/alandicted/project" class="btn btn-primary">Return to Projects</a>
                        </div>
                    </body>
                </html>
                """

            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output)
            worksheet = workbook.add_worksheet('Projects')

            headers = ['Project ID', 'Date', 'Buyer', 'Destination', 'Item (Supply ID)', 'Quantity', 'Status']
            for col, header in enumerate(headers):
                worksheet.write(0, col, header)

            for row_num, project in enumerate(projects, start=1):
                status_display = dict(project._fields['status'].selection).get(project.status, project.status)

                worksheet.write(row_num, 0, project.name)
                worksheet.write(row_num, 1, project.date.strftime('%Y-%m-%d') if project.date else '')
                worksheet.write(row_num, 2, project.buyer)
                worksheet.write(row_num, 3, project.destination)
                worksheet.write(row_num, 4, project.item_id.name if project.item_id else '')
                worksheet.write(row_num, 5, project.quantity)
                worksheet.write(row_num, 6, status_display)

            workbook.close()

            output.seek(0)
            excel_data = output.read()

            excelhttpheaders = [
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', 'attachment; filename=projects_export.xlsx')
            ]

            return request.make_response(excel_data, headers=excelhttpheaders)
        except Exception as e:
            return f"""
            <html>
                <head>
                    <title>Error</title>
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
                </head>
                <body>
                    <div class="container mt-5">
                        <div class="alert alert-danger">
                            <h4>Error exporting projects to Excel</h4>
                            <p>{str(e)}</p>
                        </div>
                        <a href="/alandicted/project" class="btn btn-primary">Return to Projects</a>
                    </div>
                </body>
            </html>
            """
