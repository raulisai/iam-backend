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


def update_latest_snapshot_with_health_data(data):
    """Update the latest snapshot with raw health data from mobile.
    
    Processes raw health data, filters null values, and formats numeric fields.
    Only updates non-null fields in the most recent snapshot.
    
    Args:
        data (dict): Raw health data from mobile app.
    
    Returns:
        tuple: JSON response with updated snapshot and status code.
    """
    try:
        user_id = request.user.get('user_id')
        
        # Get the latest snapshot to use previous values when needed
        from services.stats_service import get_latest_snapshot
        latest_snapshot = get_latest_snapshot(user_id)
        
        # Process and format the data
        processed_data = {}
        
        # Handle snapshot_at
        if data.get('snapshot_at'):
            processed_data['snapshot_at'] = data['snapshot_at']
        
        # Handle numeric metrics with decimal formatting (2 decimals)
        numeric_fields = ['energy', 'stamina', 'strength', 'flexibility', 'attention', 
                         'score_body', 'score_mind']
        for field in numeric_fields:
            if data.get(field) is not None:
                try:
                    processed_data[field] = round(float(data[field]), 2)
                except (ValueError, TypeError):
                    pass  # Skip invalid values
        
        # Handle steps_daily first (needed for calorie calculation)
        steps_value = 0
        if data.get('steps_daily') is not None:
            try:
                steps_value = int(float(data['steps_daily']))
                processed_data['steps_daily'] = str(steps_value)
            except (ValueError, TypeError):
                pass
        
        # Handle calories_burned - calculate from steps if calories = 0 or not provided
        if data.get('calories_burned') is not None:
            try:
                calories_value = float(data['calories_burned'])
                
                # If calories is 0 or very low and we have steps, calculate it
                if calories_value < 1 and steps_value > 0:
                    # Formula: 1 step ≈ 0.04 calories (average person)
                    # This varies by weight, but 0.04 is a good average
                    calories_value = steps_value * 0.04
                
                processed_data['calories_burned'] = str(round(calories_value, 2))
            except (ValueError, TypeError):
                # If error but we have steps, calculate anyway
                if steps_value > 0:
                    calories_value = steps_value * 0.04
                    processed_data['calories_burned'] = str(round(calories_value, 2))
        elif steps_value > 0:
            # No calories provided but have steps
            calories_value = steps_value * 0.04
            processed_data['calories_burned'] = str(round(calories_value, 2))
        
        # Handle heart_rate - use previous value if not provided or null
        if data.get('heart_rate') is not None:
            try:
                heart_rate_value = float(data['heart_rate'])
                processed_data['heart_rate'] = str(round(heart_rate_value, 2))
            except (ValueError, TypeError):
                # If invalid and we have a previous snapshot, use that value
                if latest_snapshot and latest_snapshot.get('heart_rate'):
                    processed_data['heart_rate'] = latest_snapshot['heart_rate']
        else:
            # No heart_rate provided, use previous value if available
            if latest_snapshot and latest_snapshot.get('heart_rate'):
                processed_data['heart_rate'] = latest_snapshot['heart_rate']
        
        # Handle sleep_score - convert milliseconds to hours
        sleep_quality = None
        if data.get('sleep_score') is not None:
            try:
                sleep_value = float(data['sleep_score'])
                
                # Convert from milliseconds to hours
                # ms -> seconds -> minutes -> hours
                if sleep_value > 1000000:  # If in milliseconds
                    sleep_seconds = sleep_value / 1000
                    sleep_minutes = sleep_seconds / 60
                    sleep_hours = sleep_minutes / 60
                else:
                    # Assume it's already in a smaller unit
                    sleep_hours = sleep_value
                
                # Store hours as string with 2 decimals
                processed_data['sleep_score'] = str(round(sleep_hours, 2))
                
                # Determine sleep quality based on hours
                # Optimal: 7-9 hours = "bueno"
                # Acceptable: 6-7 or 9-10 hours = "estable"
                # Poor: <6 or >10 hours = "malo"
                if 7 <= sleep_hours <= 9:
                    sleep_quality = "bueno"
                elif (6 <= sleep_hours < 7) or (9 < sleep_hours <= 10):
                    sleep_quality = "estable"
                else:
                    sleep_quality = "malo"
            except (ValueError, TypeError):
                pass
        
        # Handle model_version
        if data.get('model_version'):
            processed_data['model_version'] = data['model_version']
        
        # Handle inputs (keep as JSONB object)
        # Add sleep quality to inputs if we calculated it
        inputs_data = data.get('inputs') if data.get('inputs') is not None else {}
        
        # Add calculated sleep quality to inputs
        if sleep_quality:
            if isinstance(inputs_data, dict):
                inputs_data['sleep_quality'] = sleep_quality
            else:
                inputs_data = {'sleep_quality': sleep_quality}
        
        # Only set inputs if we have data
        if inputs_data:
            processed_data['inputs'] = inputs_data
        
        # If no valid data to update, return error
        if not processed_data:
            return jsonify({'error': 'No valid data to update'}), 400
        
        # Import the service function
        from services.stats_service import update_latest_snapshot
        
        # Update or create snapshot
        snapshot = update_latest_snapshot(user_id, processed_data)
        
        if not snapshot:
            return jsonify({'error': 'Failed to update snapshot'}), 500
        
        return jsonify(snapshot), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
