# Deployment Guide - Saylani AI Decision Support System

## Pre-Deployment Checklist

### 1. System Requirements Verification
- [ ] Python 3.8+ installed
- [ ] At least 4GB RAM available
- [ ] 500MB free disk space
- [ ] Windows/Linux/macOS compatible

### 2. Data Preparation
- [ ] Historical case data in CSV format
- [ ] Minimum 1,000 cases (100,000+ recommended)
- [ ] Data includes all required columns
- [ ] Data quality validated

### 3. Environment Setup
- [ ] Virtual environment created
- [ ] All dependencies installed
- [ ] No conflicting packages

---

## Deployment Steps

### Step 1: Initial Setup (First Time Only)

#### Windows
```bash
# Run the automated setup script
run_first_time.bat
```

#### Linux/Mac
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Train the AI engine
python train_engine.py

# Launch dashboard
streamlit run dashboard/app.py
```

**Expected Duration**: 5-10 minutes

### Step 2: Verify Training

After training completes, verify:
- ✅ No error messages
- ✅ Model files created in `engine/model_cache/`
- ✅ Training summary shows correct case count
- ✅ Embeddings file size ~40-50MB

### Step 3: Test the System

#### Test 1: Dashboard Access
1. Dashboard should open in browser automatically
2. URL: `http://localhost:8501`
3. Verify all sections load correctly

#### Test 2: Sample Prediction
1. Fill in the new applicant form with test data
2. Click "Get AI Recommendation"
3. Verify recommendation appears within 2 seconds
4. Check explanation is detailed and makes sense

#### Test 3: API Integration
```python
python example_integration.py
```
Verify output shows recommendation and explanation.

### Step 4: Backend Integration

#### Option A: Direct API Calls
```python
from engine.predictor import get_ai_decision_verdict

result = get_ai_decision_verdict(case_data)
```

#### Option B: REST API (Future Version)
```python
import requests

response = requests.post('http://localhost:5000/predict', json=case_data)
result = response.json()
```

### Step 5: Staff Training

#### For Decision Officers
1. **Dashboard Navigation** (15 minutes)
   - How to access the dashboard
   - Understanding the interface
   - Navigating different sections

2. **Case Evaluation** (20 minutes)
   - Entering case information
   - Interpreting AI recommendations
   - Understanding confidence scores
   - Reading explanations

3. **Using Similar Cases** (15 minutes)
   - Reviewing similar historical cases
   - Understanding similarity scores
   - Learning from patterns

4. **Analytics Review** (10 minutes)
   - Viewing historical trends
   - Understanding approval rates
   - Income distribution analysis

#### For Developers
1. **API Integration** (30 minutes)
   - Understanding the API
   - Integration examples
   - Error handling
   - Testing

2. **System Maintenance** (20 minutes)
   - Model retraining
   - Performance monitoring
   - Troubleshooting

---

## Production Deployment

### Server Requirements

#### Minimum Specs
- CPU: 2 cores
- RAM: 4GB
- Storage: 10GB
- OS: Ubuntu 20.04 LTS or Windows Server 2019

#### Recommended Specs
- CPU: 4 cores
- RAM: 8GB
- Storage: 20GB SSD
- OS: Ubuntu 22.04 LTS

### Security Considerations

1. **Network Security**
   - Dashboard accessible only on internal network
   - No external internet access required
   - Firewall rules configured

2. **Data Security**
   - All data stored locally
   - No cloud services used
   - Encrypted storage recommended

3. **Access Control**
   - User authentication (to be implemented)
   - Role-based permissions
   - Audit logging

### Monitoring

#### System Health
```bash
# Check if dashboard is running
curl http://localhost:8501

# Monitor memory usage
# Windows:
tasklist | findstr python

# Linux:
ps aux | grep python
```

#### Performance Metrics
- Average prediction time
- Memory usage
- Confidence score distribution
- User satisfaction ratings

---

## Maintenance Schedule

### Daily
- [ ] Verify dashboard is accessible
- [ ] Check for any error logs
- [ ] Monitor prediction latency

### Weekly
- [ ] Review confidence score trends
- [ ] Collect feedback from officers
- [ ] Check disk space usage

### Monthly
- [ ] Retrain model with new cases
- [ ] Review and update documentation
- [ ] Analyze recommendation accuracy
- [ ] Update system if needed

### Quarterly
- [ ] Full system audit
- [ ] Performance optimization
- [ ] User training refresher
- [ ] Backup all data and models

---

## Backup and Recovery

### Backup Procedure

#### What to Backup
1. Historical case data (CSV file)
2. Trained model files (`engine/model_cache/`)
3. Configuration files
4. Custom modifications

#### Backup Schedule
- **Daily**: Incremental backup of new cases
- **Weekly**: Full system backup
- **Monthly**: Offsite backup

#### Backup Script (Windows)
```batch
@echo off
set BACKUP_DIR=D:\Backups\Saylani-AI\%date:~-4,4%%date:~-10,2%%date:~-7,2%
mkdir %BACKUP_DIR%
xcopy /E /I /Y "engine\model_cache" "%BACKUP_DIR%\model_cache"
copy "Saylani_data (1)(Sheet1).csv" "%BACKUP_DIR%\"
echo Backup completed: %BACKUP_DIR%
```

### Recovery Procedure

1. **Stop the dashboard**
2. **Restore model files** to `engine/model_cache/`
3. **Restore data file** to project root
4. **Restart dashboard**
5. **Verify with test prediction**

---

## Troubleshooting Production Issues

### Issue: Dashboard Won't Start

**Symptoms**: Error when running `run_dashboard.bat`

**Solutions**:
1. Check if virtual environment is activated
2. Verify all dependencies installed: `pip list`
3. Check port 8501 is not in use
4. Review error logs

### Issue: Slow Predictions

**Symptoms**: Predictions take > 5 seconds

**Solutions**:
1. Check CPU/RAM usage
2. Verify model is cached (not reloading)
3. Close unnecessary applications
4. Consider upgrading hardware

### Issue: Low Confidence Scores

**Symptoms**: Most predictions have < 60% confidence

**Solutions**:
1. Retrain with more recent data
2. Verify data quality
3. Check if case patterns have changed
4. Consider adjusting `top_k` parameter

### Issue: Out of Memory

**Symptoms**: System crashes during prediction

**Solutions**:
1. Reduce `top_k` parameter
2. Close other applications
3. Upgrade RAM
4. Use smaller batch sizes

---

## Scaling Considerations

### Handling More Users

#### Current Capacity
- 10 simultaneous users
- 100 predictions/hour

#### Scaling Options

**Option 1: Vertical Scaling**
- Upgrade to 16GB RAM
- Use faster CPU
- SSD storage

**Option 2: Horizontal Scaling**
- Deploy multiple instances
- Load balancer
- Shared model cache

**Option 3: Optimization**
- Reduce embedding dimension
- Use faster model
- Implement caching

---

## Update Procedure

### Minor Updates (Bug Fixes)

1. **Backup current system**
2. **Download update files**
3. **Replace affected files**
4. **Test with sample cases**
5. **Deploy to production**

### Major Updates (New Features)

1. **Test in staging environment**
2. **Train staff on new features**
3. **Schedule maintenance window**
4. **Backup everything**
5. **Deploy update**
6. **Verify all features**
7. **Monitor for issues**

---

## Support Contacts

### Technical Issues
- **Email**: tech-support@saylani.org.pk
- **Phone**: +92-XXX-XXXXXXX
- **Hours**: 9 AM - 5 PM (Mon-Fri)

### Emergency Contact
- **24/7 Hotline**: +92-XXX-XXXXXXX
- **For**: System down, data loss, critical bugs

---

## Success Metrics

### Key Performance Indicators (KPIs)

1. **System Uptime**: > 99%
2. **Prediction Latency**: < 2 seconds
3. **Confidence Score**: > 80% average
4. **User Satisfaction**: > 4/5 rating
5. **Recommendation Accuracy**: > 70% alignment with final decisions

### Monthly Reporting

Generate monthly report including:
- Total predictions made
- Average confidence score
- Approval vs. rejection distribution
- System uptime
- User feedback summary
- Issues encountered and resolved

---

## Compliance and Audit

### Data Privacy
- All data stored locally
- No external transmission
- GDPR/local regulations compliant

### Audit Trail
- All predictions logged
- Timestamp and user recorded
- Explanation saved
- Similar cases documented

### Regular Audits
- Quarterly review of recommendations
- Bias detection analysis
- Fairness metrics
- Model performance evaluation

---

**Deployment Guide Version 1.0**  
**Last Updated**: 2024-11-24  
**Next Review**: 2025-02-24
