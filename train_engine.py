"""
Training script for Saylani AI Decision Engine
"""
import os
import sys
from utils.data_preprocessor import load_historical_data, clean_data, get_data_summary
from engine.ai_engine import SaylaniAIEngine


def train_engine():
    """Train the AI engine on historical data"""
    print("\n" + "="*70)
    print("🎓 SAYLANI AI DECISION ENGINE - TRAINING")
    print("="*70)
    
    # Load data
    data_path = "Saylani_data (1)(Sheet1).csv"
    
    if not os.path.exists(data_path):
        print(f"\n❌ Error: Data file not found at {data_path}")
        print("   Please ensure the CSV file is in the project root directory")
        return False
    
    print(f"\n📂 Loading data from: {data_path}")
    historical_data = load_historical_data(data_path)
    
    # Display summary
    print(get_data_summary(historical_data))
    
    # Clean data
    print("🧹 Cleaning data...")
    historical_data = clean_data(historical_data)
    print("✓ Data cleaned")
    
    # Initialize and train engine
    engine = SaylaniAIEngine(model_name='all-MiniLM-L6-v2')
    engine.train(historical_data)
    
    # Save trained engine
    engine.save('engine/model_cache')
    
    print("\n" + "="*70)
    print("✅ TRAINING COMPLETE!")
    print("="*70)
    print("\n📌 Next Steps:")
    print("   1. Run 'run_dashboard.bat' to launch the dashboard")
    print("   2. Or use the API in your backend:")
    print("      from engine.predictor import get_ai_decision_verdict")
    print("\n")
    
    return True


if __name__ == "__main__":
    success = train_engine()
    sys.exit(0 if success else 1)
