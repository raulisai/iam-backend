"""Statistics service for performance snapshots and metrics."""
from lib.db import get_supabase
from datetime import datetime, timedelta


def get_metric_catalog(domain=None):
    """Get all metrics from catalog, optionally filtered by domain.
    
    Args:
        domain (str, optional): Filter by domain ('body', 'mind', 'system').
    
    Returns:
        list: List of metrics.
    """
    supabase = get_supabase()
    query = supabase.from_('metric_catalog').select('*')
    
    if domain:
        query = query.eq('domain', domain)
    
    res = query.order('metric_key').execute()
    return res.data


def get_metric_by_key(metric_key):
    """Get a specific metric from catalog.
    
    Args:
        metric_key (str): The metric key.
    
    Returns:
        dict: Metric data or None.
    """
    supabase = get_supabase()
    res = supabase.from_('metric_catalog').select('*').eq('metric_key', metric_key).execute()
    return res.data[0] if res.data else None


def create_metric(data):
    """Create a new metric in catalog.
    
    Args:
        data (dict): Metric data.
    
    Returns:
        dict: Created metric.
    """
    supabase = get_supabase()
    res = supabase.from_('metric_catalog').insert(data).execute()
    return res.data[0] if res.data else None


def update_metric(metric_key, data):
    """Update a metric in catalog.
    
    Args:
        metric_key (str): The metric key.
        data (dict): Updated metric data.
    
    Returns:
        dict: Updated metric.
    """
    supabase = get_supabase()
    res = supabase.from_('metric_catalog').update(data).eq('metric_key', metric_key).execute()
    return res.data[0] if res.data else None


def delete_metric(metric_key):
    """Delete a metric from catalog.
    
    Args:
        metric_key (str): The metric key.
    
    Returns:
        dict: Deleted metric.
    """
    supabase = get_supabase()
    res = supabase.from_('metric_catalog').delete().eq('metric_key', metric_key).execute()
    return res.data[0] if res.data else None


def get_user_snapshots(user_id, start_date=None, end_date=None, limit=100):
    """Get performance snapshots for a user.
    
    Args:
        user_id (str): User ID.
        start_date (str, optional): Start date filter (ISO format).
        end_date (str, optional): End date filter (ISO format).
        limit (int): Maximum number of results.
    
    Returns:
        list: List of performance snapshots.
    """
    supabase = get_supabase()
    query = supabase.from_('performance_snapshots').select('*').eq('user_id', user_id)
    
    if start_date:
        query = query.gte('snapshot_at', start_date)
    if end_date:
        query = query.lte('snapshot_at', end_date)
    
    res = query.order('snapshot_at', desc=True).limit(limit).execute()
    return res.data


def get_snapshot_by_id(snapshot_id):
    """Get a specific performance snapshot.
    
    Args:
        snapshot_id (str): Snapshot ID.
    
    Returns:
        dict: Snapshot data or None.
    """
    supabase = get_supabase()
    res = supabase.from_('performance_snapshots').select('*').eq('id', snapshot_id).execute()
    return res.data[0] if res.data else None


def create_snapshot(data):
    """Create a new performance snapshot.
    
    Args:
        data (dict): Snapshot data including user_id and metrics.
    
    Returns:
        dict: Created snapshot.
    """
    supabase = get_supabase()
    
    # Ensure snapshot_at is set
    if 'snapshot_at' not in data:
        data['snapshot_at'] = datetime.now().isoformat()
    
    res = supabase.from_('performance_snapshots').insert(data).execute()
    return res.data[0] if res.data else None


def update_snapshot(snapshot_id, data):
    """Update a performance snapshot.
    
    Args:
        snapshot_id (str): Snapshot ID.
        data (dict): Updated snapshot data.
    
    Returns:
        dict: Updated snapshot.
    """
    supabase = get_supabase()
    res = supabase.from_('performance_snapshots').update(data).eq('id', snapshot_id).execute()
    return res.data[0] if res.data else None


def delete_snapshot(snapshot_id):
    """Delete a performance snapshot.
    
    Args:
        snapshot_id (str): Snapshot ID.
    
    Returns:
        dict: Deleted snapshot.
    """
    supabase = get_supabase()
    res = supabase.from_('performance_snapshots').delete().eq('id', snapshot_id).execute()
    return res.data[0] if res.data else None


def get_latest_snapshot(user_id):
    """Get the most recent performance snapshot for a user.
    
    Args:
        user_id (str): User ID.
    
    Returns:
        dict: Latest snapshot or None.
    """
    supabase = get_supabase()
    res = (supabase.from_('performance_snapshots')
           .select('*')
           .eq('user_id', user_id)
           .order('snapshot_at', desc=True)
           .limit(1)
           .execute())
    return res.data[0] if res.data else None


def get_stats_summary(user_id, days=30):
    """Get aggregated statistics summary for a user over a period.
    
    Args:
        user_id (str): User ID.
        days (int): Number of days to look back.
    
    Returns:
        dict: Summary statistics.
    """
    start_date = (datetime.now() - timedelta(days=days)).isoformat()
    snapshots = get_user_snapshots(user_id, start_date=start_date, limit=1000)
    
    if not snapshots:
        return {
            'count': 0,
            'period_days': days,
            'averages': {},
            'latest': None
        }
    
    # Calculate averages for numeric fields
    numeric_fields = ['energy', 'stamina', 'strength', 'flexibility', 
                     'attention', 'score_body', 'score_mind']
    
    averages = {}
    for field in numeric_fields:
        values = [s.get(field) for s in snapshots if s.get(field) is not None]
        if values:
            averages[field] = {
                'avg': sum(values) / len(values),
                'min': min(values),
                'max': max(values),
                'latest': snapshots[0].get(field)
            }
    
    return {
        'count': len(snapshots),
        'period_days': days,
        'start_date': start_date,
        'end_date': snapshots[0].get('snapshot_at') if snapshots else None,
        'averages': averages,
        'latest': snapshots[0] if snapshots else None
    }


def update_latest_snapshot(user_id, data):
    """Update the most recent performance snapshot for a user with partial data.
    
    Only updates fields that are not None. If no snapshot exists, creates a new one.
    
    Args:
        user_id (str): User ID.
        data (dict): Partial snapshot data (only non-null values will be updated).
    
    Returns:
        dict: Updated or created snapshot.
    """
    supabase = get_supabase()
    
    # Get the latest snapshot
    latest = get_latest_snapshot(user_id)
    
    # Filter out None values from data
    filtered_data = {k: v for k, v in data.items() if v is not None and k != 'user_id'}
    
    if latest:
        # Update existing snapshot
        res = supabase.from_('performance_snapshots').update(filtered_data).eq('id', latest['id']).execute()
        return res.data[0] if res.data else None
    else:
        # Create new snapshot if none exists
        filtered_data['user_id'] = user_id
        if 'snapshot_at' not in filtered_data:
            filtered_data['snapshot_at'] = datetime.now().isoformat()
        res = supabase.from_('performance_snapshots').insert(filtered_data).execute()
        return res.data[0] if res.data else None
