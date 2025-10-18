"""Task template controller for handling task template operations."""
from flask import jsonify
from services.task_template_service import (
    get_all_task_templates,
    get_task_template_by_id,
    get_task_template_by_key,
    get_templates_by_category,
    get_templates_by_created_by,
    create_task_template,
    update_task_template,
    delete_task_template
)


def get_all_templates():
    """Get all task templates.
    
    Returns:
        tuple: JSON response with templates and status code.
    """
    templates = get_all_task_templates()
    return jsonify(templates), 200


def get_template_by_id(template_id):
    """Get template by ID.
    
    Args:
        template_id (str): Template ID.
    
    Returns:
        tuple: JSON response with template and status code.
    """
    template = get_task_template_by_id(template_id)
    
    if template is None:
        return jsonify({'error': 'Template not found'}), 404
    
    return jsonify(template), 200


def get_template_by_key(key):
    """Get template by key.
    
    Args:
        key (str): Template key.
    
    Returns:
        tuple: JSON response with template and status code.
    """
    template = get_task_template_by_key(key)
    
    if template is None:
        return jsonify({'error': 'Template not found'}), 404
    
    return jsonify(template), 200


def get_templates_by_cat(category):
    """Get templates by category.
    
    Args:
        category (str): Category filter.
    
    Returns:
        tuple: JSON response with templates and status code.
    """
    templates = get_templates_by_category(category)
    return jsonify(templates), 200


def get_templates_by_creator(created_by):
    """Get templates by created_by filter.
    
    Args:
        created_by (str): Creator identifier (e.g., 'system', 'bot-<id>', '<user-id>').
    
    Returns:
        tuple: JSON response with templates and status code.
    """
    templates = get_templates_by_created_by(created_by)
    return jsonify(templates), 200


def create_template(data):
    """Create a new task template.
    
    Args:
        data (dict): Template data.
    
    Returns:
        tuple: JSON response with created template and status code.
    """
    required_fields = ['key', 'name', 'category', 'desc']
    
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    template = create_task_template(data)
    
    if template is None:
        return jsonify({'error': 'Failed to create template'}), 500
    
    return jsonify(template), 201


def update_template(template_id, data):
    """Update a task template.
    
    Args:
        template_id (str): Template ID.
        data (dict): Updated data.
    
    Returns:
        tuple: JSON response with updated template and status code.
    """
    # Remove ID from update data
    data.pop('id', None)
    
    template = update_task_template(template_id, data)
    
    if template is None:
        return jsonify({'error': 'Template not found or update failed'}), 404
    
    return jsonify(template), 200


def delete_template(template_id):
    """Delete a task template.
    
    Args:
        template_id (str): Template ID.
    
    Returns:
        tuple: JSON response with deleted template and status code.
    """
    template = delete_task_template(template_id)
    
    if template is None:
        return jsonify({'error': 'Template not found'}), 404
    
    return jsonify(template), 200
