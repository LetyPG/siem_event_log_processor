// SIEM Event Dashboard - Client-side JavaScript

// API endpoints
const API = {
    events: '/api/events',
    stats: '/api/events/stats',
    recent: '/api/events/recent'
};

// Initialize dashboard on page load
document.addEventListener('DOMContentLoaded', () => {
    loadStatistics();
    loadEvents();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    document.getElementById('refreshBtn').addEventListener('click', () => {
        loadStatistics();
        loadEvents();
    });

    document.getElementById('applyFilters').addEventListener('click', applyFilters);
    document.getElementById('clearFilters').addEventListener('click', clearFilters);

    // Apply filters on Enter key
    document.getElementById('ipFilter').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') applyFilters();
    });
}

// Load statistics from API
async function loadStatistics() {
    try {
        const response = await fetch(API.stats);
        const data = await response.json();

        if (data.success) {
            const stats = data.statistics;

            // Update stat cards
            document.getElementById('totalEvents').textContent = stats.total_events;
            document.getElementById('highThreat').textContent = stats.high_threat;
            document.getElementById('mediumThreat').textContent = stats.medium_threat;
            document.getElementById('lowThreat').textContent = stats.low_threat;

            // Update last updated time
            if (stats.last_updated) {
                document.getElementById('lastUpdated').textContent = stats.last_updated;
            }
        }
    } catch (error) {
        console.error('Error loading statistics:', error);
        showError('Failed to load statistics');
    }
}

// Load events from API
async function loadEvents(filters = {}) {
    try {
        // Build query string
        const params = new URLSearchParams();
        if (filters.threat_level) params.append('threat_level', filters.threat_level);
        if (filters.source_ip) params.append('source_ip', filters.source_ip);
        if (filters.limit) params.append('limit', filters.limit);

        const url = `${API.events}?${params.toString()}`;
        const response = await fetch(url);
        const data = await response.json();

        if (data.success) {
            displayEvents(data.events);
            document.getElementById('eventCount').textContent = `${data.count} events`;
        }
    } catch (error) {
        console.error('Error loading events:', error);
        showError('Failed to load events');
    }
}

// Display events in table
function displayEvents(events) {
    const tbody = document.getElementById('eventsTableBody');

    if (events.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="loading">No events found</td></tr>';
        return;
    }

    tbody.innerHTML = events.map(event => `
        <tr>
            <td>${event.datetime || 'N/A'}</td>
            <td>${event.source_ip || 'N/A'}</td>
            <td>${event.destination_ip || 'N/A'}</td>
            <td>${event.port || 'N/A'}</td>
            <td>${event.event_type || 'N/A'}</td>
            <td>${event.priority || 'N/A'}</td>
            <td>${getThreatBadge(event.threat_level)}</td>
        </tr>
    `).join('');
}

// Get threat level badge HTML
function getThreatBadge(threatLevel) {
    const level = threatLevel || 'Unknown';
    const className = `threat-badge threat-${level.toLowerCase()}`;

    const icons = {
        'High': '🔴',
        'Medium': '🟡',
        'Low': '🟢',
        'Unknown': '⚪'
    };

    return `<span class="${className}">${icons[level] || '⚪'} ${level}</span>`;
}

// Apply filters
function applyFilters() {
    const filters = {
        threat_level: document.getElementById('threatFilter').value,
        source_ip: document.getElementById('ipFilter').value.trim(),
        limit: document.getElementById('limitFilter').value
    };

    loadEvents(filters);
}

// Clear filters
function clearFilters() {
    document.getElementById('threatFilter').value = '';
    document.getElementById('ipFilter').value = '';
    document.getElementById('limitFilter').value = '100';
    loadEvents();
}

// Show error message
function showError(message) {
    const tbody = document.getElementById('eventsTableBody');
    tbody.innerHTML = `<tr><td colspan="7" class="loading" style="color: #ef4444;">${message}</td></tr>`;
}

// Auto-refresh every 30 seconds (optional)
// setInterval(() => {
//     loadStatistics();
//     loadEvents();
// }, 30000);
