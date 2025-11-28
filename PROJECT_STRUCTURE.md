# 📁 Project Structure - Saylani AI Decision Support System

```
Saylani-MVP-AI-System/
│
├── 📄 README.md                          # Main documentation (13KB)
├── 📄 QUICKSTART.md                      # 5-minute setup guide (5KB)
├── 📄 DEPLOYMENT.md                      # Production deployment guide (9KB)
├── 📄 CHANGELOG.md                       # Version history (2KB)
├── 📄 .gitignore                         # Git ignore rules
│
├── 📊 Saylani_data (1)(Sheet1).csv      # Historical case data (18MB, 100K+ cases)
│
├── 🔧 requirements.txt                   # Python dependencies
├── 🔧 setup.py                          # Package setup configuration
├── 🔧 train_engine.py                   # Training script
│
├── 🚀 run_first_time.bat                # First-time setup (Windows)
├── 🚀 run_dashboard.bat                 # Quick launch (Windows)
│
├── 💡 example_integration.py            # Backend integration example
│
├── 📦 engine/                           # AI Engine Package
│   ├── __init__.py
│   ├── ai_engine.py                     # Core AI engine (Sentence Transformers)
│   ├── predictor.py                     # API interface (singleton pattern)
│   └── model_cache/                     # Cached models (created after training)
│       ├── embeddings.npy               # Semantic embeddings (~40-50MB)
│       └── welfare_ai_engine.pkl        # Trained engine (~80MB)
│
├── 📦 dashboard/                        # Dashboard Package
│   ├── __init__.py
│   └── app.py                          # Streamlit dashboard (professional UI)
│
├── 📦 utils/                           # Utilities Package
│   ├── __init__.py
│   └── data_preprocessor.py            # Data loading, cleaning, validation
│
└── 📦 tests/                           # Test Suite
    └── test_engine.py                  # Comprehensive unit tests
```

---

## 📊 File Sizes & Components

### Core Files
| File | Size | Purpose |
|------|------|---------|
| `engine/ai_engine.py` | ~15KB | AI decision engine |
| `dashboard/app.py` | ~18KB | Professional dashboard |
| `utils/data_preprocessor.py` | ~4KB | Data utilities |
| `engine/predictor.py` | ~5KB | API interface |

### Documentation
| File | Size | Content |
|------|------|---------|
| `README.md` | 13KB | Complete documentation |
| `QUICKSTART.md` | 5KB | 5-minute setup guide |
| `DEPLOYMENT.md` | 9KB | Production deployment |
| `CHANGELOG.md` | 2KB | Version history |

### Data & Models (After Training)
| File | Size | Description |
|------|------|-------------|
| `Saylani_data (1)(Sheet1).csv` | 18MB | 100K historical cases |
| `engine/model_cache/embeddings.npy` | ~45MB | Semantic embeddings |
| `engine/model_cache/welfare_ai_engine.pkl` | ~80MB | Trained engine |
| Sentence Transformer model | ~80MB | Downloaded on first run |

**Total Size**: ~300MB (including all models and data)

---

## 🔄 Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    TRAINING PHASE                            │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
    ┌───────────────────────────────────────┐
    │  Load Historical Data (CSV)            │
    │  • 100,000+ cases                      │
    │  • Income, family size, feedback       │
    └───────────────┬───────────────────────┘
                    │
                    ▼
    ┌───────────────────────────────────────┐
    │  Clean & Validate Data                 │
    │  • Handle missing values               │
    │  • Standardize text                    │
    └───────────────┬───────────────────────┘
                    │
                    ▼
    ┌───────────────────────────────────────┐
    │  Generate Semantic Embeddings          │
    │  • Sentence Transformers               │
    │  • 384-dimensional vectors             │
    └───────────────┬───────────────────────┘
                    │
                    ▼
    ┌───────────────────────────────────────┐
    │  Cache Models & Embeddings             │
    │  • Save to engine/model_cache/         │
    │  • Fast subsequent loads               │
    └───────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   PREDICTION PHASE                           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
    ┌───────────────────────────────────────┐
    │  New Case Input                        │
    │  • Dashboard form or API call          │
    └───────────────┬───────────────────────┘
                    │
                    ▼
    ┌───────────────────────────────────────┐
    │  Generate Case Embedding               │
    │  • Same model as training              │
    └───────────────┬───────────────────────┘
                    │
                    ▼
    ┌───────────────────────────────────────┐
    │  Calculate Similarities                │
    │  • Cosine similarity                   │
    │  • Find top 20 matches                 │
    └───────────────┬───────────────────────┘
                    │
                    ▼
    ┌───────────────────────────────────────┐
    │  Analyze Similar Cases                 │
    │  • Count approved vs rejected          │
    │  • Calculate confidence                │
    └───────────────┬───────────────────────┘
                    │
                    ▼
    ┌───────────────────────────────────────┐
    │  Generate Explanation                  │
    │  • Pattern analysis                    │
    │  • Income comparisons                  │
    │  • Similar case details                │
    └───────────────┬───────────────────────┘
                    │
                    ▼
    ┌───────────────────────────────────────┐
    │  Return Result                         │
    │  • Recommendation (APPROVE/REJECT)     │
    │  • Confidence score                    │
    │  • Detailed explanation                │
    │  • Similar cases                       │
    └───────────────────────────────────────┘
```

---

## 🎯 Component Responsibilities

### 1. AI Engine (`engine/ai_engine.py`)
**Purpose**: Core machine learning logic

**Responsibilities**:
- Load and manage Sentence Transformer model
- Generate semantic embeddings
- Calculate cosine similarities
- Find top-K similar cases
- Generate recommendations
- Create detailed explanations
- Cache models for performance

**Key Methods**:
- `train(historical_data)` - Train on historical cases
- `predict(new_case, top_k=20)` - Generate recommendation
- `save(save_dir)` - Save trained model
- `load(save_dir)` - Load trained model

### 2. API Interface (`engine/predictor.py`)
**Purpose**: Simple backend integration

**Responsibilities**:
- Singleton pattern for efficiency
- Simple function call interface
- Error handling
- Result formatting

**Key Functions**:
- `get_ai_decision_verdict(case_data)` - Main API function
- `get_engine()` - Get/create engine instance
- `test_prediction()` - Test utility

### 3. Dashboard (`dashboard/app.py`)
**Purpose**: User interface for decision officers

**Responsibilities**:
- New case evaluation form
- AI recommendation display
- Explanation visualization
- Similar cases table
- Historical analytics
- Interactive charts

**Key Sections**:
- New Applicant Evaluation
- AI Recommendation Display
- Detailed Explanation
- Similar Cases Table
- Historical Analytics

### 4. Data Utilities (`utils/data_preprocessor.py`)
**Purpose**: Data handling and preparation

**Responsibilities**:
- Load CSV data
- Validate data quality
- Clean missing values
- Prepare case text
- Generate statistics

**Key Functions**:
- `load_historical_data(file_path)`
- `validate_data(df)`
- `clean_data(df)`
- `prepare_case_text(case_data)`
- `get_data_summary(df)`

### 5. Tests (`tests/test_engine.py`)
**Purpose**: Quality assurance

**Responsibilities**:
- Unit tests for all components
- Edge case testing
- Performance validation
- Error handling verification

**Test Classes**:
- `TestDataPreprocessor` - Data utilities
- `TestAIEngine` - AI engine
- `TestEdgeCases` - Edge cases

---

## 🔐 Security & Privacy

### Data Privacy
```
┌─────────────────────────────────────────┐
│  ALL DATA STAYS LOCAL                   │
│  ✅ No external API calls               │
│  ✅ No cloud services                   │
│  ✅ No data transmission                │
│  ✅ 100% offline operation              │
└─────────────────────────────────────────┘
```

### Access Control (Future)
- User authentication
- Role-based permissions
- Audit logging
- Session management

---

## ⚡ Performance Characteristics

### Training Phase
- **Duration**: 3-5 minutes (100K cases)
- **Memory**: ~2GB peak
- **CPU**: Moderate usage
- **Storage**: ~300MB total

### Prediction Phase
- **Latency**: 1-2 seconds
- **Memory**: ~1.2GB
- **CPU**: Low usage
- **Throughput**: 100+ predictions/hour

### Scalability
- **Current**: 10 simultaneous users
- **Max**: 50 users (with optimization)
- **Cases**: Tested up to 500K cases

---

## 🛠️ Technology Stack

### Core ML
- **Sentence Transformers** (2.2.0+)
  - Model: all-MiniLM-L6-v2
  - Size: 80MB
  - Dimension: 384

### Data Processing
- **Pandas** (1.5.0+) - Data manipulation
- **NumPy** (1.23.0+) - Numerical operations
- **Scikit-learn** (1.2.0+) - Similarity calculations

### Dashboard
- **Streamlit** (1.28.0+) - Web interface
- **Plotly** (5.17.0+) - Interactive charts

### Utilities
- **Joblib** (1.3.0+) - Model caching
- **tqdm** (4.65.0+) - Progress bars
- **PyTorch** (2.0.0+) - Deep learning backend

---

## 📈 Future Enhancements

### Version 1.1 (Planned)
- Multi-language support (Urdu)
- Batch prediction API
- PDF export of recommendations
- Advanced filtering

### Version 1.2 (Planned)
- Custom model training UI
- A/B testing framework
- SMS notifications
- Mobile-responsive design

### Version 2.0 (Planned)
- Multi-model ensemble
- Active learning
- Automated retraining
- REST API server
- SHAP explainability

---

## 📞 Support & Resources

### Documentation
- `README.md` - Complete guide
- `QUICKSTART.md` - 5-minute setup
- `DEPLOYMENT.md` - Production deployment
- `CHANGELOG.md` - Version history

### Examples
- `example_integration.py` - Backend integration
- `tests/test_engine.py` - Testing examples

### Support
- **Email**: tech@saylani.org.pk
- **Phone**: +92-XXX-XXXXXXX

---

**Project Structure v1.0** | Last Updated: 2024-11-24
