import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const API_BASE = 'http://localhost:8000';

function Dashboard() {
  const [currentData, setCurrentData] = useState(null);
  const [historicalData, setHistoricalData] = useState(null);
  const [filters, setFilters] = useState({ providers: [], environments: [], resource_types: [] });
  const [selectedProvider, setSelectedProvider] = useState('');
  const [selectedEnvironment, setSelectedEnvironment] = useState('');
  const [selectedResourceType, setSelectedResourceType] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch all data
  const fetchAllData = async () => {
    setLoading(true);
    setError(null);
    try {
      // Build query parameters
      const params = new URLSearchParams();
      if (selectedProvider) params.append('provider', selectedProvider);
      if (selectedEnvironment) params.append('environment', selectedEnvironment);
      if (selectedResourceType) params.append('resource_type', selectedResourceType);

      const queryString = params.toString() ? `?${params.toString()}` : '';

      // Fetch current usage
      const currentRes = await axios.get(`${API_BASE}/api/current${queryString}`);
      setCurrentData(currentRes.data);

      // Fetch historical data (last 30 days)
      const historicalRes = await axios.get(`${API_BASE}/api/historical${queryString}`);
      setHistoricalData(historicalRes.data);

      // Fetch filter options (only once)
      if (filters.providers.length === 0) {
        const filterRes = await axios.get(`${API_BASE}/api/filters`);
        setFilters(filterRes.data);
      }

    } catch (err) {
      console.error('Error fetching data:', err);
      setError('Failed to load dashboard data. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  // Fixed: Added the eslint disable comment to resolve the warning
  useEffect(() => {
    fetchAllData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedProvider, selectedEnvironment, selectedResourceType]);

  if (loading && !currentData) {
    return (
      <div style={{ padding: '20px', textAlign: 'center' }}>
        <h2>Loading Dashboard...</h2>
        <p>Fetching cloud cost data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: '20px', textAlign: 'center', color: 'red' }}>
        <h2>⚠️ Error</h2>
        <p>{error}</p>
        <button onClick={fetchAllData}>Retry</button>
      </div>
    );
  }

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>☁️ DevOps Dashboard</h1>
      <p>Multi-Cloud Resource & Cost Monitoring</p>

      {/* Filters */}
      <div style={{ display: 'flex', gap: '15px', marginBottom: '20px', flexWrap: 'wrap' }}>
        <div>
          <label>Provider: </label>
          <select value={selectedProvider} onChange={(e) => setSelectedProvider(e.target.value)}>
            <option value="">All</option>
            {filters.providers.map(p => <option key={p} value={p}>{p}</option>)}
          </select>
        </div>
        <div>
          <label>Environment: </label>
          <select value={selectedEnvironment} onChange={(e) => setSelectedEnvironment(e.target.value)}>
            <option value="">All</option>
            {filters.environments.map(e => <option key={e} value={e}>{e}</option>)}
          </select>
        </div>
        <div>
          <label>Resource Type: </label>
          <select value={selectedResourceType} onChange={(e) => setSelectedResourceType(e.target.value)}>
            <option value="">All</option>
            {filters.resource_types.map(r => <option key={r} value={r}>{r}</option>)}
          </select>
        </div>
        <button onClick={fetchAllData} style={{ padding: '5px 15px', cursor: 'pointer' }}>
          Refresh
        </button>
      </div>

      {/* Metric Cards */}
      {currentData && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '15px', marginBottom: '30px' }}>
          <div style={{ background: '#f0f4ff', padding: '15px', borderRadius: '8px', borderLeft: '4px solid #0066cc' }}>
            <h3>💰 Total Cost</h3>
            <p style={{ fontSize: '24px', fontWeight: 'bold', margin: '5px 0' }}>${currentData.total_cost.toFixed(2)}</p>
          </div>
          <div style={{ background: '#f0fff0', padding: '15px', borderRadius: '8px', borderLeft: '4px solid #00aa00' }}>
            <h3>🖥️ Avg CPU</h3>
            <p style={{ fontSize: '24px', fontWeight: 'bold', margin: '5px 0' }}>{currentData.avg_cpu.toFixed(1)}%</p>
          </div>
          <div style={{ background: '#fff5f0', padding: '15px', borderRadius: '8px', borderLeft: '4px solid #cc6600' }}>
            <h3>🧠 Avg Memory</h3>
            <p style={{ fontSize: '24px', fontWeight: 'bold', margin: '5px 0' }}>{currentData.avg_memory.toFixed(1)}%</p>
          </div>
          <div style={{ background: '#f5f0ff', padding: '15px', borderRadius: '8px', borderLeft: '4px solid #8800aa' }}>
            <h3>📦 Resources</h3>
            <p style={{ fontSize: '24px', fontWeight: 'bold', margin: '5px 0' }}>{currentData.total_resources}</p>
          </div>
        </div>
      )}

      {/* Historical Chart */}
      {historicalData && historicalData.labels.length > 0 ? (
        <div style={{ background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
          <h3>📈 Cost Trends (Last 30 Days)</h3>
          <div style={{ height: '300px' }}>
            <Line
              data={{
                labels: historicalData.labels,
                datasets: historicalData.datasets
              }}
              options={{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                  legend: {
                    position: 'top',
                  },
                  title: {
                    display: false,
                  },
                },
                scales: {
                  y: {
                    beginAtZero: true,
                    ticks: {
                      callback: function(value) {
                        return '$' + value.toFixed(2);
                      }
                    }
                  }
                }
              }}
            />
          </div>
        </div>
      ) : (
        <p style={{ textAlign: 'center', color: '#666' }}>No historical data available.</p>
      )}

      <div style={{ marginTop: '20px', color: '#888', fontSize: '12px', textAlign: 'center' }}>
        Data refreshed: {new Date().toLocaleString()}
      </div>
    </div>
  );
}

export default Dashboard;

