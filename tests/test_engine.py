"""
Unit tests for Saylani AI Decision Engine
"""
import unittest
import pandas as pd
import numpy as np
from engine.ai_engine import SaylaniAIEngine
from utils.data_preprocessor import clean_data, validate_data, prepare_case_text


class TestDataPreprocessor(unittest.TestCase):
    """Test data preprocessing functions"""
    
    def setUp(self):
        """Create sample data for testing"""
        self.sample_data = pd.DataFrame({
            'case_id': ['2024-00001', '2024-00002'],
            'income': [15000, 25000],
            'family_members': [8, 6],
            'enquiry_feedback': ['Poor condition', 'Clean house'],
            'verification_notes': ['CNIC verified', 'Bills checked'],
            'decision_officer_comment': ['Approve', 'Reject'],
            'final_decision': ['Approved', 'Rejected'],
            'aid_amount': [10000, 0]
        })
    
    def test_clean_data(self):
        """Test data cleaning"""
        cleaned = clean_data(self.sample_data)
        self.assertEqual(len(cleaned), len(self.sample_data))
        self.assertFalse(cleaned['enquiry_feedback'].isnull().any())
    
    def test_validate_data(self):
        """Test data validation"""
        stats = validate_data(self.sample_data)
        self.assertEqual(stats['total_cases'], 2)
        self.assertEqual(stats['approved_cases'], 1)
        self.assertEqual(stats['rejected_cases'], 1)
        self.assertEqual(stats['approval_rate'], 50.0)
    
    def test_prepare_case_text(self):
        """Test case text preparation"""
        case_dict = {
            'income': 15000,
            'family_members': 8,
            'enquiry_feedback': 'Poor condition'
        }
        text = prepare_case_text(case_dict)
        self.assertIn('15000', text)
        self.assertIn('8', text)
        self.assertIn('Poor condition', text)


class TestAIEngine(unittest.TestCase):
    """Test AI engine functionality"""
    
    def setUp(self):
        """Create sample data and engine"""
        self.sample_data = pd.DataFrame({
            'case_id': [f'2024-{i:05d}' for i in range(100)],
            'income': np.random.randint(10000, 60000, 100),
            'family_members': np.random.randint(2, 12, 100),
            'enquiry_feedback': ['Poor condition'] * 50 + ['Clean house'] * 50,
            'verification_notes': ['CNIC verified'] * 100,
            'decision_officer_comment': ['Approve'] * 60 + ['Reject'] * 40,
            'final_decision': ['Approved'] * 60 + ['Rejected'] * 40,
            'aid_amount': [10000] * 60 + [0] * 40
        })
        
        self.engine = SaylaniAIEngine()
    
    def test_engine_initialization(self):
        """Test engine initialization"""
        self.assertIsNotNone(self.engine)
        self.assertFalse(self.engine.is_trained)
    
    def test_engine_training(self):
        """Test engine training"""
        self.engine.train(self.sample_data)
        self.assertTrue(self.engine.is_trained)
        self.assertIsNotNone(self.engine.embeddings)
        self.assertEqual(len(self.engine.embeddings), len(self.sample_data))
    
    def test_prediction(self):
        """Test prediction functionality"""
        self.engine.train(self.sample_data)
        
        test_case = {
            'income': 15000,
            'family_members': 8,
            'enquiry_feedback': 'Poor condition',
            'verification_notes': 'CNIC verified',
            'decision_officer_comment': 'Approve'
        }
        
        result = self.engine.predict(test_case)
        
        self.assertIn('ai_recommendation', result)
        self.assertIn(result['ai_recommendation'], ['APPROVED', 'REJECTED'])
        self.assertIn('confidence', result)
        self.assertGreaterEqual(result['confidence'], 0)
        self.assertLessEqual(result['confidence'], 1)
        self.assertIn('explanation', result)
        self.assertIn('top_similar_cases', result)
    
    def test_prediction_without_training(self):
        """Test that prediction fails without training"""
        test_case = {'income': 15000, 'family_members': 8}
        
        with self.assertRaises(ValueError):
            self.engine.predict(test_case)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""
    
    def test_missing_data(self):
        """Test handling of missing data"""
        data = pd.DataFrame({
            'income': [15000, None, 25000],
            'family_members': [8, 6, None],
            'enquiry_feedback': ['Test', None, 'Test'],
            'final_decision': ['Approved', 'Rejected', 'Approved']
        })
        
        cleaned = clean_data(data)
        self.assertFalse(cleaned['income'].isnull().any())
        self.assertFalse(cleaned['family_members'].isnull().any())
    
    def test_extreme_values(self):
        """Test handling of extreme values"""
        engine = SaylaniAIEngine()
        
        sample_data = pd.DataFrame({
            'income': [100, 1000000],
            'family_members': [1, 20],
            'enquiry_feedback': ['Test'] * 2,
            'verification_notes': ['Test'] * 2,
            'decision_officer_comment': ['Test'] * 2,
            'final_decision': ['Approved', 'Rejected']
        })
        
        engine.train(sample_data)
        
        test_case = {
            'income': 500000,
            'family_members': 15,
            'enquiry_feedback': 'Test'
        }
        
        result = engine.predict(test_case, top_k=2)
        self.assertIsNotNone(result)


def run_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("🧪 RUNNING TESTS FOR SAYLANI AI DECISION ENGINE")
    print("="*70 + "\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestDataPreprocessor))
    suite.addTests(loader.loadTestsFromTestCase(TestAIEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED")
    print("="*70 + "\n")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests()
