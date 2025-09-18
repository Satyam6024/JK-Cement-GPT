// Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// Global state
let uploadedFiles = [];
let currentAnalysisType = 'general';

// Initialize application
document.addEventListener('DOMContentLoaded', function () {
    initializeApp();
    setupEventListeners();
    checkSystemHealth();
    loadStoredFiles();
});

function initializeApp() {
    // Check connection status
    updateConnectionStatus();

    // Load system stats
    loadSystemStats();
}

function setupEventListeners() {
    // Tab switching
    document.querySelectorAll('.tab-btn, .nav-link').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const tabName = this.dataset.tab;
            switchTab(tabName);
        });
    });

    // File upload
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');

    uploadArea.addEventListener('click', () => fileInput.click());
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleFileDrop);
    fileInput.addEventListener('change', handleFileSelect);

    // Query submission
    document.getElementById('querySubmit').addEventListener('click', submitQuery);
    document.getElementById('queryInput').addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && e.ctrlKey) {
            submitQuery();
        }
    });

    // Analysis type selection
    document.querySelectorAll('.analysis-option').forEach(option => {
        option.addEventListener('click', function () {
            document.querySelectorAll('.analysis-option').forEach(opt => opt.classList.remove('active'));
            this.classList.add('active');
            currentAnalysisType = this.dataset.type;
        });
    });

    // Insights generation
    document.getElementById('generateInsights').addEventListener('click', generateInsights);
}

// Tab switching
function switchTab(tabName) {
    // Update navigation
    document.querySelectorAll('.tab-btn, .nav-link').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tabName);
    });

    // Update content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.toggle('active', content.id === `${tabName}-tab`);
    });

    // Load data for specific tabs
    if (tabName === 'files') {
        loadFilesList();
    } else if (tabName === 'insights') {
        updateInsightFileSelect();
    }
}

// File upload handling
function handleDragOver(e) {
    e.preventDefault();
    e.currentTarget.classList.add('dragover');
}

function handleDragLeave(e) {
    e.currentTarget.classList.remove('dragover');
}

function handleFileDrop(e) {
    e.preventDefault();
    e.currentTarget.classList.remove('dragover');
    const files = Array.from(e.dataTransfer.files);
    uploadFiles(files);
}

function handleFileSelect(e) {
    const files = Array.from(e.target.files);
    uploadFiles(files);
}

async function uploadFiles(files) {
    const progressBar = document.getElementById('progressBar');
    const progressFill = document.getElementById('progressFill');
    const uploadStatus = document.getElementById('uploadStatus');

    progressBar.style.display = 'block';
    uploadStatus.innerHTML = '';

    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const progress = ((i + 1) / files.length) * 100;

        try {
            progressFill.style.width = `${progress}%`;
            await uploadSingleFile(file);

            uploadStatus.innerHTML += `
                        <div class="file-item slide-in" style="margin: 0.5rem 0; background: rgba(72, 187, 120, 0.1); border-left: 3px solid var(--success-color);">
                            <span><i class="fas fa-check-circle" style="color: var(--success-color);"></i> ${file.name} uploaded successfully</span>
                        </div>
                    `;
        } catch (error) {
            uploadStatus.innerHTML += `
                        <div class="file-item slide-in" style="margin: 0.5rem 0; background: rgba(245, 101, 101, 0.1); border-left: 3px solid var(--error-color);">
                            <span><i class="fas fa-exclamation-circle" style="color: var(--error-color);"></i> Failed to upload ${file.name}: ${error.message}</span>
                        </div>
                    `;
        }
    }

    setTimeout(() => {
        progressBar.style.display = 'none';
        loadStoredFiles();
    }, 1000);
}

async function uploadSingleFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/upload`, {
        method: 'POST',
        body: formData
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();

    if (result.status === 'error') {
        throw new Error(result.error);
    }

    // Store file info
    uploadedFiles.push({
        id: result.file_id,
        name: file.name,
        type: result.metadata?.file_type,
        uploadedAt: new Date(),
        validation: result.validation
    });

    return result;
}

// Query handling
async function submitQuery() {
    const queryInput = document.getElementById('queryInput');
    const querySubmit = document.getElementById('querySubmit');
    const queryResults = document.getElementById('queryResults');

    const query = queryInput.value.trim();
    if (!query) return;

    // Show loading state
    querySubmit.innerHTML = '<div class="loading"></div>';
    querySubmit.disabled = true;

    try {
        const response = await fetch(`${API_BASE_URL}/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: query,
                analysis_type: currentAnalysisType
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        displayQueryResults(result);

    } catch (error) {
        queryResults.innerHTML = `
                    <div class="result-card" style="border-color: var(--error-color);">
                        <div class="result-header">
                            <h4 style="color: var(--error-color);">
                                <i class="fas fa-exclamation-triangle"></i> Error
                            </h4>
                        </div>
                        <div class="result-content">
                            ${error.message}
                        </div>
                    </div>
                `;
    } finally {
        querySubmit.innerHTML = '<i class="fas fa-paper-plane"></i>';
        querySubmit.disabled = false;
    }
}

function displayQueryResults(result) {
    const queryResults = document.getElementById('queryResults');
    const confidence = result.confidence || 0;
    const confidenceClass = confidence > 0.7 ? 'confidence-high' : confidence > 0.4 ? 'confidence-medium' : 'confidence-low';

    queryResults.innerHTML = `
                <div class="result-card fade-in">
                    <div class="result-header">
                        <h4><i class="fas fa-brain"></i> Analysis Results</h4>
                        <span class="confidence-badge ${confidenceClass}">
                            ${Math.round(confidence * 100)}% Confidence
                        </span>
                    </div>
                    
                    <div class="result-content">
                        ${formatAnalysisText(result.analysis)}
                    </div>

                    ${result.trends ? `
                        <div class="sources">
                            <h5><i class="fas fa-trending-up"></i> Trends Identified</h5>
                            ${result.trends.map(trend => `<div class="source-item">${trend}</div>`).join('')}
                        </div>
                    ` : ''}

                    ${result.comparisons ? `
                        <div class="sources">
                            <h5><i class="fas fa-balance-scale"></i> Comparisons</h5>
                            ${result.comparisons.map(comp => `<div class="source-item">${comp}</div>`).join('')}
                        </div>
                    ` : ''}

                    ${result.sources && result.sources.length > 0 ? `
                        <div class="sources">
                            <h5><i class="fas fa-file-alt"></i> Data Sources</h5>
                            ${result.sources.map(source => `
                                <div class="source-item">
                                    <strong>${source.filename || 'Unknown'}</strong> 
                                    (${source.file_type || 'Unknown type'})
                                </div>
                            `).join('')}
                        </div>
                    ` : ''}
                </div>
            `;
}

function formatAnalysisText(text) {
    return text
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/(\d+\.?\d*%)/g, '<span style="color: var(--primary-color); font-weight: bold;">$1</span>');
}

// File management
async function loadFilesList() {
    const filesList = document.getElementById('filesList');
    const fileCount = document.getElementById('fileCount');

    try {
        filesList.innerHTML = '<div style="text-align: center; padding: 2rem;"><div class="loading"></div> Loading files...</div>';

        // In a real app, you'd fetch from an API endpoint
        // For now, we'll use the uploaded files array

        if (uploadedFiles.length === 0) {
            filesList.innerHTML = `
                        <div style="text-align: center; padding: 3rem; color: var(--text-secondary);">
                            <i class="fas fa-folder-open" style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.3;"></i>
                            <p>No files uploaded yet</p>
                            <button class="btn" onclick="switchTab('upload')">Upload Your First File</button>
                        </div>
                    `;
            return;
        }

        filesList.innerHTML = uploadedFiles.map(file => `
                    <div class="file-item slide-in">
                        <div class="file-info">
                            <i class="file-icon ${getFileIcon(file.type)}"></i>
                            <div>
                                <div style="font-weight: 500;">${file.name}</div>
                                <div style="font-size: 0.8rem; color: var(--text-secondary);">
                                    ${file.type?.toUpperCase()} • ${formatDate(file.uploadedAt)}
                                </div>
                            </div>
                        </div>
                        <div class="file-actions">
                            <button class="action-btn" onclick="viewFileInsights('${file.id}')">
                                <i class="fas fa-chart-line"></i> Insights
                            </button>
                            <button class="action-btn" onclick="queryFile('${file.id}')">
                                <i class="fas fa-search"></i> Query
                            </button>
                            <button class="action-btn" onclick="deleteFile('${file.id}')">
                                <i class="fas fa-trash"></i> Delete
                            </button>
                        </div>
                    </div>
                `).join('');

        fileCount.textContent = `${uploadedFiles.length} files`;

    } catch (error) {
        filesList.innerHTML = `
                    <div style="text-align: center; padding: 2rem; color: var(--error-color);">
                        <i class="fas fa-exclamation-triangle"></i> Error loading files
                    </div>
                `;
    }
}

function getFileIcon(type) {
    const icons = {
        'csv': 'fas fa-table',
        'xlsx': 'fas fa-file-excel',
        'xls': 'fas fa-file-excel',
        'json': 'fas fa-code',
        'pdf': 'fas fa-file-pdf',
        'docx': 'fas fa-file-word',
        'xml': 'fas fa-code',
        'db': 'fas fa-database',
        'sqlite': 'fas fa-database',
        'sqlite3': 'fas fa-database',
        'accdb': 'fas fa-database',
        'mdb': 'fas fa-database'
    };
    return icons[type] || 'fas fa-file';
}

function formatDate(date) {
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    }).format(date);
}

// Insights generation
async function generateInsights() {
    const fileSelect = document.getElementById('insightFileSelect');
    const insightsResults = document.getElementById('insightsResults');
    const generateBtn = document.getElementById('generateInsights');

    const fileId = fileSelect.value;
    if (!fileId) return;

    generateBtn.innerHTML = '<div class="loading"></div> Generating...';
    generateBtn.disabled = true;

    try {
        const response = await fetch(`${API_BASE_URL}/insights/${fileId}`, {
            method: 'GET'
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        displayInsights(result);

    } catch (error) {
        insightsResults.innerHTML = `
                    <div class="card" style="border-color: var(--error-color); margin-top: 2rem;">
                        <h4 style="color: var(--error-color);">
                            <i class="fas fa-exclamation-triangle"></i> Error Generating Insights
                        </h4>
                        <p>${error.message}</p>
                    </div>
                `;
    } finally {
        generateBtn.innerHTML = '<i class="fas fa-magic"></i> Generate Insights';
        generateBtn.disabled = false;
    }
}

function displayInsights(result) {
    const insightsResults = document.getElementById('insightsResults');

    insightsResults.innerHTML = `
                <div class="card fade-in" style="margin-top: 2rem;">
                    <h3 style="color: var(--primary-color); margin-bottom: 1.5rem;">
                        <i class="fas fa-lightbulb"></i> Business Insights
                    </h3>
                    
                    <div class="result-content" style="margin-bottom: 2rem;">
                        ${formatAnalysisText(result.insights)}
                    </div>

                    ${result.recommendations && result.recommendations.length > 0 ? `
                        <div class="sources">
                            <h5><i class="fas fa-bullseye"></i> Key Recommendations</h5>
                            ${result.recommendations.map(rec => `<div class="source-item">${rec}</div>`).join('')}
                        </div>
                    ` : ''}

                    <div style="margin-top: 2rem; padding-top: 2rem; border-top: 1px solid rgba(102, 126, 234, 0.1);">
                        <h5 style="margin-bottom: 1rem;"><i class="fas fa-info-circle"></i> Data Summary</h5>
                        <p style="color: var(--text-secondary); font-size: 0.9rem;">${result.data_summary}</p>
                    </div>
                </div>
            `;
}

// Utility functions
function updateInsightFileSelect() {
    const select = document.getElementById('insightFileSelect');
    select.innerHTML = '<option value="">Select a file for insights...</option>';

    uploadedFiles.forEach(file => {
        const option = document.createElement('option');
        option.value = file.id;
        option.textContent = `${file.name} (${file.type?.toUpperCase()})`;
        select.appendChild(option);
    });
}

async function loadSystemStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/stats`);
        if (response.ok) {
            const stats = await response.json();
            document.getElementById('totalDocs').textContent = stats.documents_processed || 0;
            document.getElementById('systemStatus').textContent = 'Online';
        }
    } catch (error) {
        document.getElementById('systemStatus').textContent = 'Offline';
        document.getElementById('systemStatus').style.color = 'var(--error-color)';
    }
}

async function checkSystemHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const isHealthy = response.ok;
        updateConnectionStatus(isHealthy);
    } catch (error) {
        updateConnectionStatus(false);
    }
}

function updateConnectionStatus(isConnected = true) {
    const statusElement = document.getElementById('connectionStatus');
    const statusDot = document.querySelector('.status-dot');

    if (isConnected) {
        statusElement.textContent = 'Connected';
        statusDot.style.background = 'var(--success-color)';
    } else {
        statusElement.textContent = 'Disconnected';
        statusDot.style.background = 'var(--error-color)';
    }
}

function loadStoredFiles() {
    // Update file counts
    document.getElementById('totalFiles').textContent = uploadedFiles.length;

    // Update recent uploads
    const recentUploads = document.getElementById('recentUploads');
    const recent = uploadedFiles.slice(-3).reverse();

    if (recent.length === 0) {
        recentUploads.innerHTML = '<div style="color: var(--text-secondary); text-align: center; padding: 1rem;">No files uploaded yet</div>';
        return;
    }

    recentUploads.innerHTML = recent.map(file => `
                <div class="file-item" style="padding: 0.8rem;">
                    <div class="file-info">
                        <i class="${getFileIcon(file.type)}" style="color: var(--primary-color);"></i>
                        <div>
                            <div style="font-size: 0.9rem; font-weight: 500;">${file.name}</div>
                            <div style="font-size: 0.7rem; color: var(--text-secondary);">
                                ${formatDate(file.uploadedAt)}
                            </div>
                        </div>
                    </div>
                </div>
            `).join('');
}

function refreshFiles() {
    loadFilesList();
    updateInsightFileSelect();
    loadStoredFiles();
}

function viewFileInsights(fileId) {
    const select = document.getElementById('insightFileSelect');
    select.value = fileId;
    switchTab('insights');
    generateInsights();
}

function queryFile(fileId) {
    const file = uploadedFiles.find(f => f.id === fileId);
    if (file) {
        document.getElementById('queryInput').value = `Analyze the data from ${file.name}`;
        switchTab('query');
    }
}

function deleteFile(fileId) {
    if (confirm('Are you sure you want to delete this file?')) {
        uploadedFiles = uploadedFiles.filter(f => f.id !== fileId);
        refreshFiles();
    }
}

// Auto-refresh system status
setInterval(() => {
    checkSystemHealth();
    loadSystemStats();
}, 30000);

// Keyboard shortcuts
document.addEventListener('keydown', function (e) {
    if (e.ctrlKey || e.metaKey) {
        switch (e.key) {
            case '1':
                e.preventDefault();
                switchTab('upload');
                break;
            case '2':
                e.preventDefault();
                switchTab('query');
                break;
            case '3':
                e.preventDefault();
                switchTab('files');
                break;
            case '4':
                e.preventDefault();
                switchTab('insights');
                break;
        }
    }
});

// Add some sample queries for demo
const sampleQueries = [
    "What are the key trends in this dataset?",
    "Show me statistical summary of the data",
    "Identify any outliers or anomalies",
    "Compare performance across different categories",
    "What insights can you derive from this data?",
    "Generate business recommendations based on the analysis"
];

function addSampleQuery() {
    const randomQuery = sampleQueries[Math.floor(Math.random() * sampleQueries.length)];
    document.getElementById('queryInput').value = randomQuery;
}

// Add sample query button to query section
document.addEventListener('DOMContentLoaded', function () {
    const querySection = document.querySelector('#query-tab .card');
    const sampleBtn = document.createElement('button');
    sampleBtn.className = 'btn btn-secondary';
    sampleBtn.innerHTML = '<i class="fas fa-lightbulb"></i> Try Sample Query';
    sampleBtn.onclick = addSampleQuery;
    sampleBtn.style.marginTop = '1rem';
    querySection.appendChild(sampleBtn);
});