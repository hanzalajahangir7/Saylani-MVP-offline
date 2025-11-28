"""
Simple API for backend integration
Singleton pattern for efficient model loading
"""
import os
from typing import Dict
from engine.ai_engine import SaylaniAIEngine


# Global engine instance (singleton)
_engine_instance = None


def get_engine() -> SaylaniAIEngine:
    """
    Get or create the AI engine instance (singleton pattern)
    
    Returns:
        Initialized AI engine
    """
    global _engine_instance
    
    if _engine_instance is None:
        print("🚀 Initializing AI Decision Engine...")
        _engine_instance = SaylaniAIEngine()
        
        # Try to load pre-trained model
        model_dir = 'engine/model_cache'
        if os.path.exists(os.path.join(model_dir, 'welfare_ai_engine.pkl')):
            try:
                _engine_instance.load(model_dir)
                print("✓ Loaded pre-trained engine from cache")
            except Exception as e:
                print(f"⚠ Could not load cached engine: {e}")
                print("   Please run training first!")
                raise
        else:
            print("⚠ No pre-trained model found!")
            print(f"   Expected location: {model_dir}")
            print("   Please run 'run_first_time.bat' to train the model")
            raise FileNotFoundError("AI engine not trained. Run training first.")
    
    return _engine_instance


def get_ai_decision_verdict(case_data: Dict) -> Dict:
    """
    Get AI recommendation for a welfare case
    
    This is the main API function for backend integration.
    
    Args:
        case_data: Dictionary with case information containing:
            - income: Monthly income in PKR
            - family_members: Number of family members
            - enquiry_feedback: Text notes from enquiry officer
            - verification_notes: Text notes from verification officer
            - decision_officer_comment: Comments from decision officer
    
    Returns:
        Dictionary with:
            - ai_recommendation: "APPROVED" or "REJECTED"
            - confidence: Float between 0 and 1
            - explanation: Detailed text explanation
            - similar_cases_count: Number of similar cases analyzed
            - approved_matches: Number of approved similar cases
            - rejected_matches: Number of rejected similar cases
            - top_similar_cases: List of most similar historical cases
            - generated_at: Timestamp
    
    Example:
        >>> result = get_ai_decision_verdict({
        ...     "income": 12000,
        ...     "family_members": 8,
        ...     "enquiry_feedback": "Kacha house, no furniture",
        ...     "verification_notes": "CNIC valid, bills attached",
        ...     "decision_officer_comment": "Seems genuine"
        ... })
        >>> print(result['ai_recommendation'])  # "APPROVED" or "REJECTED"
        >>> print(result['confidence'])  # 0.85
    """
    try:
        engine = get_engine()
        result = engine.predict(case_data)
        return result
    except Exception as e:
        return {
            'ai_recommendation': 'ERROR',
            'confidence': 0.0,
            'explanation': f'Error generating recommendation: {str(e)}',
            'similar_cases_count': 0,
            'approved_matches': 0,
            'rejected_matches': 0,
            'top_similar_cases': [],
            'generated_at': ''
        }


# Convenience function for quick testing
def test_prediction():
    """Test the prediction API with a sample case"""
    sample_case = {
        "income": 12000,
        "family_members": 8,
        "enquiry_feedback": "Very poor condition, no stable income",
        "verification_notes": "CNIC verified, documents match",
        "decision_officer_comment": "Extreme poverty, must approve"
    }
    
    print("\n" + "="*60)
    print("🧪 Testing AI Decision Engine")
    print("="*60)
    
    result = get_ai_decision_verdict(sample_case)
    
    print(f"\n📋 Test Case:")
    print(f"   Income: PKR {sample_case['income']:,}")
    print(f"   Family: {sample_case['family_members']} members")
    
    print(f"\n🤖 AI Verdict:")
    print(f"   Recommendation: {result['ai_recommendation']}")
    print(f"   Confidence: {result['confidence']*100:.0f}%")
    
    print(f"\n📊 Analysis:")
    print(f"   Similar cases analyzed: {result['similar_cases_count']}")
    print(f"   Approved matches: {result['approved_matches']}")
    print(f"   Rejected matches: {result['rejected_matches']}")
    
    print(f"\n💡 Explanation:")
    print(result['explanation'])
    
    print("\n" + "="*60)
    
    return result


if __name__ == "__main__":
    # Run test when executed directly
    test_prediction()
