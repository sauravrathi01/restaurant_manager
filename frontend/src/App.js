import React, { useState } from 'react';
import axios from 'axios';
import { Sparkles, ChefHat, Coffee, AlertCircle, CheckCircle, Loader } from 'lucide-react';
import './App.css';

function App() {
  const [itemName, setItemName] = useState('');
  const [modelVersion, setModelVersion] = useState('gpt-3.5-turbo');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!itemName.trim()) {
      setError('Please enter a food item name');
      return;
    }

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/generate-item-details`, {
        item_name: itemName.trim(),
        model_version: modelVersion
      });

      setResult(response.data);
    } catch (err) {
      console.error('API Error:', err);
      
      if (err.response?.status === 429) {
        setError('Rate limit exceeded. Please wait a moment and try again.');
      } else if (err.response?.status === 503) {
        setError('AI service temporarily unavailable. Please try again later.');
      } else if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else {
        setError('An unexpected error occurred. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setItemName('');
    setResult(null);
    setError(null);
  };

  return (
    <div className="App">
      <div className="container">
        <header className="header">
          <div className="logo">
            <Sparkles className="logo-icon" />
            <h1>Menu Intelligence Widget</h1>
          </div>
          <p className="subtitle">
            AI-powered menu description and upsell suggestion generator
          </p>
        </header>

        <main className="main-content">
          <div className="widget-card">
            <div className="card-header">
              <ChefHat className="card-icon" />
              <h2>Generate Menu Details</h2>
            </div>

            <form onSubmit={handleSubmit} className="form">
              <div className="form-group">
                <label htmlFor="itemName">Food Item Name</label>
                <input
                  type="text"
                  id="itemName"
                  value={itemName}
                  onChange={(e) => setItemName(e.target.value)}
                  placeholder="e.g., Paneer Tikka Pizza, Butter Chicken, etc."
                  className="input"
                  disabled={isLoading}
                />
              </div>

              <div className="form-group">
                <label htmlFor="modelVersion">AI Model</label>
                <select
                  id="modelVersion"
                  value={modelVersion}
                  onChange={(e) => setModelVersion(e.target.value)}
                  className="select"
                  disabled={isLoading}
                >
                  <option value="gpt-3.5-turbo">GPT-3.5 Turbo (Faster)</option>
                  <option value="gpt-4">GPT-4 (More Creative)</option>
                </select>
              </div>

              <div className="form-actions">
                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={isLoading || !itemName.trim()}
                >
                  {isLoading ? (
                    <>
                      <Loader className="btn-icon spinning" />
                      Generating...
                    </>
                  ) : (
                    <>
                      <Sparkles className="btn-icon" />
                      Generate Details
                    </>
                  )}
                </button>
                
                {result && (
                  <button
                    type="button"
                    onClick={handleReset}
                    className="btn btn-secondary"
                  >
                    Start Over
                  </button>
                )}
              </div>
            </form>

            {error && (
              <div className="error-message">
                <AlertCircle className="error-icon" />
                <span>{error}</span>
              </div>
            )}

            {result && (
              <div className="result-section">
                <div className="result-header">
                  <CheckCircle className="success-icon" />
                  <h3>Generated Content</h3>
                  <span className="model-badge">
                    {result.model_used}
                  </span>
                </div>

                <div className="result-content">
                  <div className="result-card">
                    <h4>Menu Description</h4>
                    <p className="description">{result.description}</p>
                    <div className="word-count">
                      {result.description.split(' ').length} words
                    </div>
                  </div>

                  <div className="result-card">
                    <h4>Upsell Suggestion</h4>
                    <div className="upsell-suggestion">
                      <Coffee className="upsell-icon" />
                      <p>{result.upsell_suggestion}</p>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          <div className="info-section">
            <h3>How it works</h3>
            <div className="info-grid">
              <div className="info-item">
                <div className="info-number">1</div>
                <p>Enter your food item name</p>
              </div>
              <div className="info-item">
                <div className="info-number">2</div>
                <p>Choose your preferred AI model</p>
              </div>
              <div className="info-item">
                <div className="info-number">3</div>
                <p>Get instant menu description & upsell suggestion</p>
              </div>
            </div>
          </div>
        </main>

        <footer className="footer">
          <p>
            AI-Powered Menu Intelligence Widget | 
            Designed for Restaurant POS Integration
          </p>
        </footer>
      </div>
    </div>
  );
}

export default App;
