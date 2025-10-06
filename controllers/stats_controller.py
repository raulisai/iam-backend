"""Statistics controller for handling metrics and performance snapshots."""
from flask import jsonify, request
from services.stats_service import (
    get_metric_catalog,
    get_metric_by_key,
    create_metric,
    update_metric,
    delete_metric,
    get_user_snapshots,
    get_snapshot_by_id,
    create_snapshot,
    update_snapshot,
    delete_snapshot,
    get_latest_snapshot,
    get_stats_summary
)


# ========== METRIC CATALOG ENDPOINTS ==========

def get_all_metrics(domain=None):
    """Get all metrics from catalog.
    
    Args:
        domain (str, optional): Filter by domain.
    
    Returns:
        tuple: JSON response with metrics and status code.
    """
    try:
        metrics = get_metric_catalog(domain)
        return jsonify(metrics), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_metric(metric_key):
    """Get a specific metric.
    
    Args:
        metric_key (str): The metric key.
    
    Returns:
        tuple: JSON response with metric data and status code.
    """
    try:
        metric = get_metric_by_key(metric_key)
        if not metric:
            return jsonify({'error': 'Metric not found'}), 404
        return jsonify(metric), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def create_new_metric(data):
    """Create a new metric.
    
    Args:
        data (dict): Metric data.
    
    Returns:
        tuple: JSON response with created metric and status code.
    """
    try:
        required_fields = ['metric_key', 'domain', 'display_name']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Validate domain
        if data['domain'] not in ['body', 'mind', 'system']:
            return jsonify({'error': 'Invalid domain. Must be body, mind, or system'}), 400
        
        # Validate agg_method if provided
        if 'agg_method' in data and data['agg_method'] not in ['sum', 'avg', 'min', 'max', 'last']:
            return jsonify({'error': 'Invalid aggregation method'}), 400
        
        metric = create_metric(data)
        return jsonify(metric), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def update_metric_by_key(metric_key, data):
    """Update a metric.
    
    Args:
        metric_key (str): The metric key.
        data (dict): Updated metric data.
    
    Returns:
        tuple: JSON response with updated metric and status code.
    """
    try:
        # Validate domain if provided
        if 'domain' in data and data['domain'] not in ['body', 'mind', 'system']:
            return jsonify({'error': 'Invalid domain'}), 400
        
        # Validate agg_method if provided
        if 'agg_method' in data and data['agg_method'] not in ['sum', 'avg', 'min', 'max', 'last']:
            return jsonify({'error': 'Invalid aggregation method'}), 400
        
        metric = update_metric(metric_key, data)
        if not metric:
            return jsonify({'error': 'Metric not found'}), 404
        return jsonify(metric), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def delete_metric_by_key(metric_key):
    """Delete a metric.
    
    Args:
        metric_key (str): The metric key.
    
    Returns:
        tuple: JSON response with deleted metric and status code.
    """
    try:
        metric = delete_metric(metric_key)
        if not metric:
            return jsonify({'error': 'Metric not found'}), 404
        return jsonify(metric), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ========== PERFORMANCE SNAPSHOTS ENDPOINTS ==========

def get_snapshots_for_user():
    """Get performance snapshots for authenticated user.
    
    Returns:
        tuple: JSON response with snapshots and status code.
    """
    try:
        user_id = request.user.get('user_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        limit = request.args.get('limit', 100, type=int)
        
        snapshots = get_user_snapshots(user_id, start_date, end_date, limit)
        return jsonify(snapshots), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_snapshot(snapshot_id):
    """Get a specific snapshot.
    
    Args:
        snapshot_id (str): Snapshot ID.
    
    Returns:
        tuple: JSON response with snapshot data and status code.
    """
    try:
        snapshot = get_snapshot_by_id(snapshot_id)
        if not snapshot:
            return jsonify({'error': 'Snapshot not found'}), 404
        
        # Verify ownership
        user_id = request.user.get('user_id')
        if snapshot['user_id'] != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        return jsonify(snapshot), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def create_new_snapshot(data):
    """Create a new performance snapshot.
    
    Args:
        data (dict): Snapshot data.
    
    Returns:
        tuple: JSON response with created snapshot and status code.
    """
    try:
        # Ensure user_id is set from authenticated user
        user_id = request.user.get('user_id')
        data['user_id'] = user_id
        
        snapshot = create_snapshot(data)
        return jsonify(snapshot), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def update_snapshot_by_id(snapshot_id, data):
    """Update a performance snapshot.
    
    Args:
        snapshot_id (str): Snapshot ID.
        data (dict): Updated snapshot data.
    
    Returns:
        tuple: JSON response with updated snapshot and status code.
    """
    try:
        # Verify ownership
        snapshot = get_snapshot_by_id(snapshot_id)
        if not snapshot:
            return jsonify({'error': 'Snapshot not found'}), 404
        
        user_id = request.user.get('user_id')
        if snapshot['user_id'] != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Don't allow changing user_id
        data.pop('user_id', None)
        data.pop('id', None)
        
        updated_snapshot = update_snapshot(snapshot_id, data)
        return jsonify(updated_snapshot), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def delete_snapshot_by_id(snapshot_id):
    """Delete a performance snapshot.
    
    Args:
        snapshot_id (str): Snapshot ID.
    
    Returns:
        tuple: JSON response with deleted snapshot and status code.
    """
    try:
        # Verify ownership
        snapshot = get_snapshot_by_id(snapshot_id)
        if not snapshot:
            return jsonify({'error': 'Snapshot not found'}), 404
        
        user_id = request.user.get('user_id')
        if snapshot['user_id'] != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        deleted_snapshot = delete_snapshot(snapshot_id)
        return jsonify(deleted_snapshot), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_user_latest_snapshot():
    """Get the latest snapshot for authenticated user.
    
    Returns:
        tuple: JSON response with latest snapshot and status code.
    """
    try:
        user_id = request.user.get('user_id')
        snapshot = get_latest_snapshot(user_id)
        if not snapshot:
            return jsonify({'message': 'No snapshots found'}), 404
        return jsonify(snapshot), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_user_stats_summary():
    """Get aggregated statistics summary for authenticated user.
    
    Returns:
        tuple: JSON response with summary and status code.
    """
    try:
        user_id = request.user.get('user_id')
        days = request.args.get('days', 30, type=int)
        summary = get_stats_summary(user_id, days)
        return jsonify(summary), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
