// URL Input and Analyze Button
const urlInput = document.getElementById('urlInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const errorAlert = document.getElementById('errorAlert');
const resultsContainer = document.getElementById('resultsContainer');

// Event Listeners
analyzeBtn.addEventListener('click', analyzeURL);
urlInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') analyzeURL();
});

// Smooth Scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
            updateActiveNavLink(this.getAttribute('href'));
        }
    });
});

function updateActiveNavLink(targetId) {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === targetId) {
            link.classList.add('active');
        }
    });
}

// Analyze URL Function
async function analyzeURL() {
    const url = urlInput.value.trim();

    // Validation
    if (!url) {
        showError('Please enter a URL');
        return;
    }

    // Ensure URL has protocol
    let processedUrl = url;
    if (!url.match(/^https?:\/\//)) {
        processedUrl = 'https://' + url;
    }

    // Show loading state
    analyzeBtn.disabled = true;
    analyzeBtn.querySelector('.btn-text').style.display = 'none';
    analyzeBtn.querySelector('.loader').classList.remove('hidden');
    errorAlert.classList.add('hidden');
    resultsContainer.classList.add('hidden');

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: processedUrl })
        });

        if (!response.ok) {
            const error = await response.json();
            showError(error.error || 'Analysis failed');
            return;
        }

        const result = await response.json();
        displayResults(result);
    } catch (error) {
        showError('Connection error: ' + error.message);
    } finally {
        analyzeBtn.disabled = false;
        analyzeBtn.querySelector('.btn-text').style.display = 'block';
        analyzeBtn.querySelector('.loader').classList.add('hidden');
    }
}

// Display Results
function displayResults(result) {
    // Update URL Display
    document.getElementById('analyzedUrl').textContent = result.url;

    // Update Prediction
    const prediction = result.prediction.toLowerCase();
    const resultHeader = document.getElementById('resultHeader');
    
    // Set icon and color based on prediction
    const iconMap = {
        'benign': '✅',
        'phishing': '🎣',
        'malware': '☠️',
        'defacement': '🔨'
    };

    const colorMap = {
        'benign': '#10b981',
        'phishing': '#ef4444',
        'malware': '#ef4444',
        'defacement': '#f59e0b'
    };

    const icon = iconMap[prediction] || '⚪';
    const color = colorMap[prediction] || '#6366f1';

    document.getElementById('resultIcon').textContent = icon;
    document.getElementById('resultIcon').style.color = color;
    document.getElementById('resultIcon').style.background = color + '20';
    
    document.getElementById('resultType').textContent = icon + ' ' + result.prediction;
    document.getElementById('resultType').style.color = color;
    document.getElementById('resultReason').textContent = result.reason;

    // Update Confidence
    const confidence = result.confidence;
    const confidenceBar = document.getElementById('confidenceBar');
    confidenceBar.style.width = '0%';
    
    setTimeout(() => {
        confidenceBar.style.width = confidence + '%';
        confidenceBar.style.background = 
            confidence >= 80 ? 'linear-gradient(90deg, #10b981, #6ee7b7)' : 
            confidence >= 50 ? 'linear-gradient(90deg, #f59e0b, #fcd34d)' :
            'linear-gradient(90deg, #ef4444, #fca5a5)';
    }, 100);

    document.getElementById('confidenceValue').textContent = confidence.toFixed(2) + '%';

    // Update Probabilities
    const probabilities = result.probabilities;
    for (const [key, value] of Object.entries(probabilities)) {
        const prob = (value * 100).toFixed(2);
        document.getElementById(`prob-${key}`).textContent = prob + '%';
        
        const bar = document.getElementById(`bar-${key}`);
        bar.style.width = '0%';
        
        setTimeout(() => {
            bar.style.width = (value * 100) + '%';
        }, 100);
    }

    // Update Features
    const features = result.features;
    updateFeatureDisplay('url_length', features.url_length + ' chars');
    updateFeatureDisplay('has_https', features.has_https ? '✅ Yes' : '❌ No');
    updateFeatureDisplay('has_ip_address', features.has_ip_address ? '⚠️ Yes' : '✅ No');
    updateFeatureDisplay('has_suspicious_keyword', features.has_suspicious_keyword ? '⚠️ Yes' : '✅ No');
    updateFeatureDisplay('num_dots', features.num_dots);
    updateFeatureDisplay('num_hyphens', features.num_hyphens);
    updateFeatureDisplay('has_at_symbol', features.has_at_symbol ? '⚠️ Yes' : '✅ No');
    updateFeatureDisplay('domain_length', features.domain_length + ' chars');

    // Show Results
    resultsContainer.classList.remove('hidden');
    
    // Scroll to results
    setTimeout(() => {
        document.getElementById('resultsContainer').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);
}

function updateFeatureDisplay(featureId, value) {
    const element = document.getElementById(`feat-${featureId}`);
    if (element) {
        element.textContent = value;
    }
}

// Show Error
function showError(message) {
    errorAlert.textContent = '❌ Error: ' + message;
    errorAlert.classList.remove('hidden');
    resultsContainer.classList.add('hidden');
}

// Analyze Example URL
function analyzeExampleURL(url) {
    urlInput.value = url;
    analyzeURL();
}

// Update Active Nav Link on Scroll
window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section');
    let current = '';

    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        if (pageYOffset >= sectionTop - 60) {
            current = section.getAttribute('id');
        }
    });

    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === '#' + current) {
            link.classList.add('active');
        }
    });
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Set first nav link as active
    document.querySelector('.nav-link').classList.add('active');
});
