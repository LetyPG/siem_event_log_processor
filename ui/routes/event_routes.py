# Controller layer - Route handlers for SIEM event dashboard

from flask import Blueprint, render_template, jsonify, request
import sys
import os

# Add parent directory to path to import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from ui.models.event_model import EventModel
from src.complex_processor_functions.combined_processor_functions import combine_read_file_normalize_timestamp_add_threat_level
import json


# Create blueprint
event_bp = Blueprint('events', __name__)

# Initialize model
event_model = EventModel()


@event_bp.route('/')
def dashboard():
    """Render the main dashboard page"""
    return render_template('dashboard.html')


@event_bp.route('/api/events')
def get_events():
    """
    Get all events or filtered events.
    
    Query parameters:
        - threat_level: Filter by threat level
        - source_ip: Filter by source IP
        - event_type: Filter by event type
        - limit: Maximum number of events (default: 100)
    """
    threat_level = request.args.get('threat_level')
    source_ip = request.args.get('source_ip')
    event_type = request.args.get('event_type')
    limit = int(request.args.get('limit', 100))
    
    events = event_model.filter_events(
        threat_level=threat_level,
        source_ip=source_ip,
        event_type=event_type,
        limit=limit
    )
    
    return jsonify({
        'success': True,
        'count': len(events),
        'events': events
    })


@event_bp.route('/api/events/stats')
def get_statistics():
    """Get event statistics"""
    stats = event_model.get_event_statistics()
    return jsonify({
        'success': True,
        'statistics': stats
    })


@event_bp.route('/api/events/recent')
def get_recent():
    """Get recent events"""
    limit = int(request.args.get('limit', 10))
    events = event_model.get_recent_events(limit=limit)
    
    return jsonify({
        'success': True,
        'count': len(events),
        'events': events
    })


@event_bp.route('/api/process', methods=['POST'])
def process_events():
    """
    Trigger event processing.
    
    Expects JSON body with:
        - file_path: Path to the event log file
    """
    try:
        data = request.get_json()
        file_path = data.get('file_path', 'events_siem.txt')
        
        # Process events using existing function
        processed_events = combine_read_file_normalize_timestamp_add_threat_level(file_path)
        
        # Save to JSON file
        with open('processed_events.json', 'w', encoding='utf-8') as f:
            json.dump(processed_events, f, indent=2)
        
        return jsonify({
            'success': True,
            'message': f'Processed {len(processed_events)} events',
            'count': len(processed_events)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
