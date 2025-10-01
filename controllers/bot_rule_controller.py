"""Bot rule controller for handling bot rule operations."""
from flask import jsonify, request
from services.bot_rule_service import (
    get_all_bot_rules,
    get_bot_rule_by_id,
    create_bot_rule,
    update_bot_rule,
    delete_bot_rule
)


def get_bot_rules():
    """Get all bot rules.
    
    Returns:
        tuple: JSON response with rules and status code.
    """
    active_only = request.args.get('active_only', 'false').lower() == 'true'
    rules = get_all_bot_rules(active_only)
    return jsonify(rules), 200


def get_rule(rule_id):
    """Get bot rule by ID.
    
    Args:
        rule_id (str): Rule ID.
    
    Returns:
        tuple: JSON response with rule and status code.
    """
    rule = get_bot_rule_by_id(rule_id)
    
    if rule is None:
        return jsonify({'error': 'Rule not found'}), 404
    
    return jsonify(rule), 200


def create_rule(data):
    """Create a new bot rule.
    
    Args:
        data (dict): Rule data.
    
    Returns:
        tuple: JSON response with created rule and status code.
    """
    required_fields = ['name', 'condition', 'action']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'name, condition, and action are required'}), 400
    
    rule = create_bot_rule(data)
    
    if rule is None:
        return jsonify({'error': 'Failed to create rule'}), 500
    
    return jsonify(rule), 201


def update_rule(rule_id, data):
    """Update a bot rule.
    
    Args:
        rule_id (str): Rule ID.
        data (dict): Updated data.
    
    Returns:
        tuple: JSON response with updated rule and status code.
    """
    data.pop('id', None)
    data.pop('created_at', None)
    
    rule = update_bot_rule(rule_id, data)
    
    if rule is None:
        return jsonify({'error': 'Rule not found or update failed'}), 404
    
    return jsonify(rule), 200


def delete_rule(rule_id):
    """Delete a bot rule.
    
    Args:
        rule_id (str): Rule ID.
    
    Returns:
        tuple: JSON response with deleted rule and status code.
    """
    rule = delete_bot_rule(rule_id)
    
    if rule is None:
        return jsonify({'error': 'Rule not found'}), 404
    
    return jsonify(rule), 200
