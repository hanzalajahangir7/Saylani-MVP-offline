"""
Example integration script showing how to use the AI engine in your backend
"""
from engine.predictor import get_ai_decision_verdict


def process_welfare_application(applicant_data):
    """
    Example function showing how to integrate AI recommendations
    into your existing welfare application processing workflow
    
    Args:
        applicant_data: Dictionary with applicant information
        
    Returns:
        Dictionary with processing result
    """
    
    # Step 1: Extract relevant data for AI analysis
    case_data = {
        "income": applicant_data.get('monthly_income'),
        "family_members": applicant_data.get('family_size'),
        "enquiry_feedback": applicant_data.get('enquiry_notes', ''),
        "verification_notes": applicant_data.get('verification_notes', ''),
        "decision_officer_comment": applicant_data.get('officer_comments', '')
    }
    
    # Step 2: Get AI recommendation
    ai_result = get_ai_decision_verdict(case_data)
    
    # Step 3: Use the recommendation in your workflow
    if ai_result['ai_recommendation'] == 'APPROVED':
        if ai_result['confidence'] >= 0.8:
            # High confidence approval
            status = "RECOMMENDED_FOR_APPROVAL"
            priority = "HIGH"
        else:
            # Low confidence - needs review
            status = "NEEDS_REVIEW"
            priority = "MEDIUM"
    else:
        if ai_result['confidence'] >= 0.8:
            # High confidence rejection
            status = "RECOMMENDED_FOR_REJECTION"
            priority = "LOW"
        else:
            # Low confidence - needs review
            status = "NEEDS_REVIEW"
            priority = "MEDIUM"
    
    # Step 4: Return result with AI insights
    return {
        'applicant_id': applicant_data.get('id'),
        'status': status,
        'priority': priority,
        'ai_recommendation': ai_result['ai_recommendation'],
        'ai_confidence': ai_result['confidence'],
        'ai_explanation': ai_result['explanation'],
        'similar_cases_count': ai_result['similar_cases_count'],
        'timestamp': ai_result['generated_at']
    }


# Example usage
if __name__ == "__main__":
    # Sample applicant data
    sample_applicant = {
        'id': 'APP-2024-12345',
        'name': 'Muhammad Ahmed',
        'monthly_income': 15000,
        'family_size': 8,
        'enquiry_notes': 'Very poor condition, no stable income, children not in school',
        'verification_notes': 'CNIC verified, utility bills attached, landlord confirmed',
        'officer_comments': 'Family seems genuinely in need, recommend approval'
    }
    
    # Process the application
    result = process_welfare_application(sample_applicant)
    
    # Display result
    print("\n" + "="*70)
    print("WELFARE APPLICATION PROCESSING RESULT")
    print("="*70)
    print(f"\nApplicant ID: {result['applicant_id']}")
    print(f"Status: {result['status']}")
    print(f"Priority: {result['priority']}")
    print(f"\nAI Recommendation: {result['ai_recommendation']}")
    print(f"AI Confidence: {result['ai_confidence']*100:.0f}%")
    print(f"Similar Cases Analyzed: {result['similar_cases_count']}")
    print(f"\nAI Explanation:\n{result['ai_explanation']}")
    print("\n" + "="*70)
