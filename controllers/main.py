# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request


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
            return request.render('alandicted_odoo.inventory_template', {})
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
    
    @http.route('/alandicted/project', type='http', auth='user', website=True)
    def project(self, **kwargs):
        try:
            # Get projects from session
            projects = request.session.get('projects', [])
            return request.render('alandicted_odoo.project_template', {'projects': projects})
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
            # Format date to display format MM/DD/YYYY
            date_obj = None
            try:
                if kwargs.get('date'):
                    from datetime import datetime
                    date_obj = datetime.strptime(kwargs.get('date'), '%Y-%m-%d')
                    formatted_date = date_obj.strftime('%m/%d/%Y')
                else:
                    formatted_date = ""
            except Exception:
                formatted_date = kwargs.get('date', '')
            
            # Generate a random project ID
            import random
            project_id = f"#{random.randint(7000, 9999)}"
            
            # Store project data in session
            if not request.session.get('projects'):
                request.session['projects'] = []
            
            new_project = {
                'project_id': project_id,
                'date': formatted_date,
                'buyer': kwargs.get('buyer', ''),
                'item': kwargs.get('item', ''),
                'quantity': kwargs.get('quantity', '0'),
                'destination': kwargs.get('destination', ''),
                'status': kwargs.get('status', 'pending')
            }
            
            projects = request.session.get('projects', [])
            projects.append(new_project)
            request.session['projects'] = projects
            
            return request.redirect('/alandicted/project')
        else:
            try:
                return request.render('alandicted_odoo.add_project_template', {})
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