# AI-Powered Menu Intelligence Widget

A lightweight, full-stack AI-powered widget that helps restaurant managers auto-generate item descriptions for digital menus and suggests upsell combinations using OpenAI's GPT models.

## 🚀 Features

- **AI-Powered Menu Descriptions**: Generate compelling, appetizing menu descriptions (max 30 words)
- **Smart Upsell Suggestions**: Get intelligent recommendations for complementary items
- **Model Toggle**: Switch between GPT-3.5 Turbo (faster) and GPT-4 (more creative)
- **Modern UI**: Beautiful, responsive interface with glassmorphism design
- **Security & Validation**: Input sanitization, rate limiting, and error handling
- **RESTful API**: Clean FastAPI backend with comprehensive documentation

## 🏗️ Architecture

```
restaurant_manager/
├── backend/                 # Python FastAPI backend
│   ├── main.py             # Main API server
│   ├── Pipfile             # Python dependencies (pipenv)
│   ├── Pipfile.lock        # Locked dependency versions
│   └── env.example         # Backend environment configuration
├── frontend/               # React frontend
│   ├── public/
│   ├── src/
│   │   ├── App.js          # Main React component
│   │   ├── App.css         # Modern styling
│   │   └── index.js        # React entry point
│   ├── package.json        # Frontend dependencies
│   └── env.example         # Frontend environment configuration
└── README.md              # This file
```

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.8+
- pipenv (install with: `pip install pipenv`)
- Node.js 16+
- OpenAI API key

### 1. Clone and Setup

```bash
git clone <repository-url>
cd restaurant_manager
```

### 2. Backend Setup

```bash
# Install pipenv if not already installed
pip install pipenv

# Install Python dependencies (including development tools)
cd backend
pipenv install --dev

# Copy environment file and configure
cp env.example .env
# Edit .env and add your OpenAI API key
```

### 3. Frontend Setup

```bash
cd frontend
npm install

# Optional: Copy environment file and configure
cp env.example .env
# Edit .env if you need to customize API URL or other settings
```

### 4. Run the Application

#### Terminal 1 - Backend
```bash
cd backend
pipenv run python main.py
# Server runs on http://localhost:8000
```

#### Terminal 2 - Frontend
```bash
cd frontend
npm start
# App runs on http://localhost:3000
```

## 🔧 Configuration

### Environment Variables

#### Backend Environment (backend/.env)

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Security Configuration
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
RATE_LIMIT=10/minute
```

#### Frontend Environment (frontend/.env) - Optional

```env
# API Configuration
REACT_APP_API_URL=http://localhost:8000
REACT_APP_API_TIMEOUT=30000

# Application Configuration
REACT_APP_NAME=Menu Intelligence Widget
REACT_APP_VERSION=1.0.0
```

### API Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health status
- `POST /generate-item-details` - Generate menu description and upsell

## 🎯 Prompt Engineering

The system uses a carefully crafted prompt for consistent AI responses:

```python
MENU_GENERATION_PROMPT = """
You are an expert restaurant menu copywriter and sales strategist. Your task is to create compelling menu descriptions and upsell suggestions.

For the given food item, provide:

1. A BRIEF, ATTRACTIVE DESCRIPTION (maximum 30 words):
   - Highlight key ingredients, flavors, and appeal
   - Use appetizing, descriptive language
   - Focus on what makes this dish special
   - Keep it concise and mouth-watering

2. ONE UPSELL SUGGESTION:
   - Suggest a complementary drink, side, or dessert
   - Make it sound irresistible and logical
   - Use persuasive but not pushy language
   - Format as "Pair it with [item]!" or similar

IMPORTANT RULES:
- Description must be exactly 30 words or less
- Use professional, appetizing language
- Avoid generic phrases like "delicious" or "tasty"
- Be specific about flavors, textures, and ingredients
- Make the upsell suggestion relevant and appealing
"""
```

## 🔒 Security Features

- **Input Validation**: Pydantic models with comprehensive validation
- **Input Sanitization**: Removes potentially harmful characters
- **Rate Limiting**: 10 requests per minute per IP
- **Error Handling**: Graceful error responses with appropriate HTTP status codes
- **CORS Protection**: Configured for frontend integration

## 📱 POS Integration

This widget is designed to integrate seamlessly with restaurant POS systems like Grafterr:

### Integration Points

1. **Menu Item Management Screen**: Add a "Generate AI Description" button
2. **Item Creation Flow**: Auto-generate descriptions during item setup
3. **Upsell Recommendations**: Display suggested combinations to staff
4. **Bulk Operations**: Generate descriptions for multiple items

### Example Integration Code

```javascript
// In your POS item management component
const generateAIDescription = async (itemName) => {
  try {
    const response = await fetch('/api/generate-item-details', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ item_name: itemName })
    });
    
    const result = await response.json();
    
    // Update your POS item with AI-generated content
    updateMenuItem({
      description: result.description,
      upsell_suggestion: result.upsell_suggestion
    });
  } catch (error) {
    console.error('AI generation failed:', error);
  }
};
```

## 🧪 Testing

### Backend Testing

#### Option 1: Simple Test (Recommended for quick testing)
```bash
# Run the simple test script
test_simple.bat
```

#### Option 2: Full Test Suite (Requires pytest)
```bash
cd backend
pipenv run pytest tests/
```

#### Option 3: Manual Testing
```bash
# Start the backend server
cd backend
pipenv run python main.py

# In another terminal, test the API
curl http://localhost:8000/health
curl -X POST http://localhost:8000/generate-item-details \
  -H "Content-Type: application/json" \
  -d '{"item_name": "Test Pizza", "model_version": "gpt-3.5-turbo"}'
```

### Frontend Testing

```bash
cd frontend
npm test
```

## 📊 API Response Format

```json
{
  "description": "A delicious fusion of authentic Indian spices and premium cheese on crispy crust.",
  "upsell_suggestion": "Pair it with a refreshing Mango Lassi!",
  "model_used": "gpt-3.5-turbo",
  "success": true
}
```

## 🚀 Deployment

### Backend Deployment

```bash
# Using uvicorn with pipenv
cd backend
pipenv run uvicorn main:app --host 0.0.0.0 --port 8000

# Using Docker
docker build -t menu-widget-backend .
docker run -p 8000:8000 menu-widget-backend
```

### Frontend Deployment

```bash
cd frontend
npm run build
# Deploy the build folder to your web server
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `http://localhost:8000/docs`
- Review the health endpoint at `http://localhost:8000/health`

## 🔮 Future Enhancements

- [ ] Multi-language support
- [ ] Custom prompt templates
- [ ] Batch processing for multiple items
- [ ] Integration with more AI providers
- [ ] Analytics dashboard
- [ ] User feedback collection
- [ ] A/B testing for different prompts
