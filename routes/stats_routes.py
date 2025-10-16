"""Statistics routes for metrics catalog and performance snapshots."""
from flask import Blueprint, request, jsonify
from controllers.stats_controller import (
    get_all_metrics,
    get_metric,
    create_new_metric,
    update_metric_by_key,
    delete_metric_by_key,
    get_snapshots_for_user,
    get_snapshot,
    create_new_snapshot,
    update_snapshot_by_id,
    delete_snapshot_by_id,
    get_user_latest_snapshot,
    get_user_stats_summary
)
from middleware.auth_middleware import token_required

# Create Blueprint for statistics routes
stats_routes = Blueprint('stats', __name__, url_prefix='/api/stats')


# ========== METRIC CATALOG ROUTES ==========

@stats_routes.route('/metrics', methods=['GET', 'OPTIONS'])
@token_required
def get_metrics():
    """
    Get all metrics from catalog.
    ---
    tags:
      - Statistics
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: query
        name: domain
        description: Filter by domain (body, mind, system)
        required: false
        type: string
        enum: [body, mind, system]
    responses:
      200:
        description: List of metrics
        schema:
          type: array
          items:
            type: object
            properties:
              metric_key:
                type: string
                example: "energy"
              domain:
                type: string
                example: "body"
              display_name:
                type: string
                example: "Energy"
              unit:
                type: string
                example: "%"
              agg_method:
                type: string
                example: "avg"
              min_value:
                type: number
                example: 0
              max_value:
                type: number
                example: 100
              created_at:
                type: string
                format: date-time
      401:
        description: Unauthorized
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    domain = request.args.get('domain')
    return get_all_metrics(domain)


@stats_routes.route('/metrics/<metric_key>', methods=['GET', 'OPTIONS'])
@token_required
def get_metric_by_key(metric_key):
    """
    Get a specific metric by key.
    ---
    tags:
      - Statistics
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: path
        name: metric_key
        description: The metric key
        required: true
        type: string
    responses:
      200:
        description: Metric data
        schema:
          type: object
          properties:
            metric_key:
              type: string
            domain:
              type: string
            display_name:
              type: string
            unit:
              type: string
            agg_method:
              type: string
            min_value:
              type: number
            max_value:
              type: number
            created_at:
              type: string
              format: date-time
      404:
        description: Metric not found
        schema:
          $ref: '#/definitions/ErrorResponse'
      401:
        description: Unauthorized
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    return get_metric(metric_key)


@stats_routes.route('/metrics', methods=['POST'])
@token_required
def create_metric():
    """
    Create a new metric in catalog.
    ---
    tags:
      - Statistics
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: body
        name: body
        description: Metric data
        required: true
        schema:
          type: object
          required:
            - metric_key
            - domain
            - display_name
          properties:
            metric_key:
              type: string
              example: "custom_metric"
              description: Unique key for the metric
            domain:
              type: string
              example: "body"
              enum: [body, mind, system]
              description: Domain category
            display_name:
              type: string
              example: "Custom Metric"
              description: Display name for the metric
            unit:
              type: string
              example: "%"
              description: Unit of measurement
            agg_method:
              type: string
              example: "avg"
              enum: [sum, avg, min, max, last]
              description: Aggregation method
            min_value:
              type: number
              example: 0
              description: Minimum allowed value
            max_value:
              type: number
              example: 100
              description: Maximum allowed value
    responses:
      201:
        description: Metric created successfully
        schema:
          type: object
          properties:
            metric_key:
              type: string
            domain:
              type: string
            display_name:
              type: string
            unit:
              type: string
            agg_method:
              type: string
            min_value:
              type: number
            max_value:
              type: number
            created_at:
              type: string
              format: date-time
      400:
        description: Invalid request
        schema:
          $ref: '#/definitions/ErrorResponse'
      401:
        description: Unauthorized
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    return create_new_metric(data)


@stats_routes.route('/metrics/<metric_key>', methods=['PUT'])
@token_required
def update_metric(metric_key):
    """
    Update a metric in catalog.
    ---
    tags:
      - Statistics
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: path
        name: metric_key
        description: The metric key
        required: true
        type: string
      - in: body
        name: body
        description: Updated metric data
        required: true
        schema:
          type: object
          properties:
            domain:
              type: string
              enum: [body, mind, system]
            display_name:
              type: string
            unit:
              type: string
            agg_method:
              type: string
              enum: [sum, avg, min, max, last]
            min_value:
              type: number
            max_value:
              type: number
    responses:
      200:
        description: Metric updated successfully
        schema:
          type: object
          properties:
            metric_key:
              type: string
            domain:
              type: string
            display_name:
              type: string
            unit:
              type: string
            agg_method:
              type: string
            min_value:
              type: number
            max_value:
              type: number
            created_at:
              type: string
              format: date-time
      400:
        description: Invalid request
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Metric not found
        schema:
          $ref: '#/definitions/ErrorResponse'
      401:
        description: Unauthorized
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    return update_metric_by_key(metric_key, data)


@stats_routes.route('/metrics/<metric_key>', methods=['DELETE'])
@token_required
def delete_metric(metric_key):
    """
    Delete a metric from catalog.
    ---
    tags:
      - Statistics
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: path
        name: metric_key
        description: The metric key
        required: true
        type: string
    responses:
      200:
        description: Metric deleted successfully
        schema:
          type: object
          properties:
            metric_key:
              type: string
      404:
        description: Metric not found
        schema:
          $ref: '#/definitions/ErrorResponse'
      401:
        description: Unauthorized
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    return delete_metric_by_key(metric_key)


# ========== PERFORMANCE SNAPSHOTS ROUTES ==========

@stats_routes.route('/snapshots', methods=['GET', 'OPTIONS'])
@token_required
def get_snapshots():
    """
    Get performance snapshots for authenticated user.
    ---
    tags:
      - Statistics
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: query
        name: start_date
        description: Start date filter (ISO format)
        required: false
        type: string
        format: date-time
      - in: query
        name: end_date
        description: End date filter (ISO format)
        required: false
        type: string
        format: date-time
      - in: query
        name: limit
        description: Maximum number of results
        required: false
        type: integer
        default: 100
    responses:
      200:
        description: List of performance snapshots
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
                format: uuid
              user_id:
                type: string
                format: uuid
              snapshot_at:
                type: string
                format: date-time
              energy:
                type: number
              stamina:
                type: number
              strength:
                type: number
              flexibility:
                type: number
              attention:
                type: number
              score_body:
                type: number
              score_mind:
                type: number
              model_version:
                type: string
              calories_burned:
                type: string
              steps_daily:
                type: string
              heart_rate:
                type: string
              sleep_score:
                type: string
              inputs:
                type: object
      401:
        description: Unauthorized
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    return get_snapshots_for_user()


@stats_routes.route('/snapshots/<snapshot_id>', methods=['GET', 'OPTIONS'])
@token_required
def get_snapshot_by_id(snapshot_id):
    """
    Get a specific performance snapshot.
    ---
    tags:
      - Statistics
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: path
        name: snapshot_id
        description: Snapshot ID
        required: true
        type: string
        format: uuid
    responses:
      200:
        description: Performance snapshot data
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            user_id:
              type: string
              format: uuid
            snapshot_at:
              type: string
              format: date-time
            energy:
              type: number
            stamina:
              type: number
            strength:
              type: number
            flexibility:
              type: number
            attention:
              type: number
            score_body:
              type: number
            score_mind:
              type: number
            model_version:
              type: string
            calories_burned:
              type: string
            steps_daily:
              type: string
            heart_rate:
              type: string
            sleep_score:
              type: string
            inputs:
              type: object
      403:
        description: Unauthorized - not owner
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Snapshot not found
        schema:
          $ref: '#/definitions/ErrorResponse'
      401:
        description: Unauthorized
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    return get_snapshot(snapshot_id)


@stats_routes.route('/snapshots', methods=['POST'])
@token_required
def create_snapshot():
    """
    Create a new performance snapshot.
    ---
    tags:
      - Statistics
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: body
        name: body
        description: Snapshot data
        required: true
        schema:
          type: object
          properties:
            snapshot_at:
              type: string
              format: date-time
              description: Timestamp of snapshot (defaults to now)
            energy:
              type: number
              example: 85.5
            stamina:
              type: number
              example: 72.3
            strength:
              type: number
              example: 68.0
            flexibility:
              type: number
              example: 55.0
            attention:
              type: number
              example: 80.0
            score_body:
              type: number
              example: 70.2
            score_mind:
              type: number
              example: 80.0
            model_version:
              type: string
              example: "v1.0"
            calories_burned:
              type: string
              example: "2500"
            steps_daily:
              type: string
              example: "10000"
            heart_rate:
              type: string
              example: "72"
            sleep_score:
              type: string
              example: "85"
            inputs:
              type: object
              description: Input metrics used for calculation
              example: {"task_count": 10, "workout_time": 60}
    responses:
      201:
        description: Snapshot created successfully
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            user_id:
              type: string
              format: uuid
            snapshot_at:
              type: string
              format: date-time
            energy:
              type: number
            stamina:
              type: number
            strength:
              type: number
            flexibility:
              type: number
            attention:
              type: number
            score_body:
              type: number
            score_mind:
              type: number
            model_version:
              type: string
            calories_burned:
              type: string
            steps_daily:
              type: string
            heart_rate:
              type: string
            sleep_score:
              type: string
            inputs:
              type: object
      400:
        description: Invalid request
        schema:
          $ref: '#/definitions/ErrorResponse'
      401:
        description: Unauthorized
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    return create_new_snapshot(data)


@stats_routes.route('/snapshots/<snapshot_id>', methods=['PUT'])
@token_required
def update_snapshot(snapshot_id):
    """
    Update a performance snapshot.
    ---
    tags:
      - Statistics
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: path
        name: snapshot_id
        description: Snapshot ID
        required: true
        type: string
        format: uuid
      - in: body
        name: body
        description: Updated snapshot data
        required: true
        schema:
          type: object
          properties:
            energy:
              type: number
            stamina:
              type: number
            strength:
              type: number
            flexibility:
              type: number
            attention:
              type: number
            score_body:
              type: number
            score_mind:
              type: number
            model_version:
              type: string
            calories_burned:
              type: string
            steps_daily:
              type: string
            heart_rate:
              type: string
            sleep_score:
              type: string
            inputs:
              type: object
    responses:
      200:
        description: Snapshot updated successfully
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            user_id:
              type: string
              format: uuid
            snapshot_at:
              type: string
              format: date-time
            energy:
              type: number
            stamina:
              type: number
            strength:
              type: number
            flexibility:
              type: number
            attention:
              type: number
            score_body:
              type: number
            score_mind:
              type: number
            model_version:
              type: string
            calories_burned:
              type: string
            steps_daily:
              type: string
            heart_rate:
              type: string
            sleep_score:
              type: string
            inputs:
              type: object
      400:
        description: Invalid request
        schema:
          $ref: '#/definitions/ErrorResponse'
      403:
        description: Unauthorized - not owner
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Snapshot not found
        schema:
          $ref: '#/definitions/ErrorResponse'
      401:
        description: Unauthorized
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    return update_snapshot_by_id(snapshot_id, data)


@stats_routes.route('/snapshots/<snapshot_id>', methods=['DELETE'])
@token_required
def delete_snapshot(snapshot_id):
    """
    Delete a performance snapshot.
    ---
    tags:
      - Statistics
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: path
        name: snapshot_id
        description: Snapshot ID
        required: true
        type: string
        format: uuid
    responses:
      200:
        description: Snapshot deleted successfully
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
      403:
        description: Unauthorized - not owner
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Snapshot not found
        schema:
          $ref: '#/definitions/ErrorResponse'
      401:
        description: Unauthorized
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    return delete_snapshot_by_id(snapshot_id)


@stats_routes.route('/snapshots/latest', methods=['GET', 'OPTIONS'])
@token_required
def get_latest_snapshot():
    """
    Get the latest performance snapshot for authenticated user.
    ---
    tags:
      - Statistics
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
    responses:
      200:
        description: Latest performance snapshot
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            user_id:
              type: string
              format: uuid
            snapshot_at:
              type: string
              format: date-time
            energy:
              type: number
            stamina:
              type: number
            strength:
              type: number
            flexibility:
              type: number
            attention:
              type: number
            score_body:
              type: number
            score_mind:
              type: number
            model_version:
              type: string
            calories_burned:
              type: string
            steps_daily:
              type: string
            heart_rate:
              type: string
            sleep_score:
              type: string
            inputs:
              type: object
      404:
        description: No snapshots found
        schema:
          type: object
          properties:
            message:
              type: string
              example: "No snapshots found"
      401:
        description: Unauthorized
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    return get_user_latest_snapshot()


@stats_routes.route('/summary', methods=['GET', 'OPTIONS'])
@token_required
def get_summary():
    """
    Get aggregated statistics summary for authenticated user.
    ---
    tags:
      - Statistics
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: query
        name: days
        description: Number of days to look back
        required: false
        type: integer
        default: 30
    responses:
      200:
        description: Statistics summary
        schema:
          type: object
          properties:
            count:
              type: integer
              description: Number of snapshots in period
              example: 30
            period_days:
              type: integer
              description: Number of days analyzed
              example: 30
            start_date:
              type: string
              format: date-time
              description: Start of analysis period
            end_date:
              type: string
              format: date-time
              description: End of analysis period
            averages:
              type: object
              description: Aggregated statistics for each metric
              properties:
                energy:
                  type: object
                  properties:
                    avg:
                      type: number
                      example: 75.5
                    min:
                      type: number
                      example: 50.0
                    max:
                      type: number
                      example: 95.0
                    latest:
                      type: number
                      example: 80.0
                stamina:
                  type: object
                  properties:
                    avg:
                      type: number
                    min:
                      type: number
                    max:
                      type: number
                    latest:
                      type: number
            latest:
              type: object
              description: Most recent snapshot
              properties:
                id:
                  type: string
                  format: uuid
                snapshot_at:
                  type: string
                  format: date-time
                energy:
                  type: number
                stamina:
                  type: number
      401:
        description: Unauthorized
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    return get_user_stats_summary()


@stats_routes.route('/snapshots/update-latest', methods=['POST', 'OPTIONS'])
@token_required
def update_latest_snapshot():
    """
    Update the latest performance snapshot with raw health data.
    
    This endpoint updates only the non-null fields in the most recent snapshot.
    If no snapshot exists, it creates a new one. Raw health data is processed and formatted.
    ---
    tags:
      - Statistics
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: body
        name: body
        description: Raw health data from mobile device
        required: true
        schema:
          type: object
          properties:
            snapshot_at:
              type: string
              format: date-time
              description: Timestamp of snapshot
              example: "2025-10-16T16:33:36.947130Z"
            energy:
              type: number
              nullable: true
              example: null
            stamina:
              type: number
              nullable: true
              example: null
            strength:
              type: number
              nullable: true
              example: null
            flexibility:
              type: number
              nullable: true
              example: null
            attention:
              type: number
              nullable: true
              example: null
            score_body:
              type: number
              nullable: true
              example: null
            score_mind:
              type: number
              nullable: true
              example: null
            model_version:
              type: string
              example: "v1.0"
            calories_burned:
              type: string
              description: Calories burned. If 0, will be calculated from steps (1 step ≈ 0.04 cal)
              example: "0.0"
            steps_daily:
              type: string
              description: Daily steps count (used for calorie calculation if needed)
              example: "94"
            heart_rate:
              type: string
              nullable: true
              description: Heart rate in BPM. If null, uses previous snapshot value
              example: "67.25"
            sleep_score:
              type: string
              description: Sleep duration in milliseconds (auto-converted to hours with quality label)
              example: "25200000"
            inputs:
              type: object
              nullable: true
              description: Additional input metrics
              example: null
    responses:
      200:
        description: Snapshot updated successfully
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            user_id:
              type: string
              format: uuid
            snapshot_at:
              type: string
              format: date-time
            energy:
              type: number
            stamina:
              type: number
            strength:
              type: number
            flexibility:
              type: number
            attention:
              type: number
            score_body:
              type: number
            score_mind:
              type: number
            model_version:
              type: string
            calories_burned:
              type: string
              example: "3.76"
            steps_daily:
              type: string
              example: "94"
            heart_rate:
              type: string
              example: "67.25"
            sleep_score:
              type: string
              description: Format - "hours | quality" (quality = malo/estable/bueno)
              example: "7.0 | bueno"
            inputs:
              type: object
      400:
        description: Invalid request or no valid data to update
        schema:
          $ref: '#/definitions/ErrorResponse'
      401:
        description: Unauthorized
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    
    from controllers.stats_controller import update_latest_snapshot_with_health_data
    return update_latest_snapshot_with_health_data(data)
