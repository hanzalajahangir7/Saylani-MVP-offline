"""
AI Decision Engine for Saylani Welfare Management System
Uses Sentence Transformers for semantic similarity matching
"""
import os
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
from typing import Dict, List, Tuple
from datetime import datetime
from tqdm import tqdm


class SaylaniAIEngine:
    """
    Explainable AI engine for welfare case decision support
    """
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize the AI engine
        
        Args:
            model_name: Name of the sentence transformer model
        """
        self.model_name = model_name
        self.model = None
        self.historical_data = None
        self.embeddings = None
        self.is_trained = False
        
        print(f"🤖 Initializing Saylani AI Decision Engine...")
        print(f"   Model: {model_name}")
    
    def load_model(self):
        """Load the sentence transformer model"""
        if self.model is None:
            print("📥 Loading sentence transformer model...")
            self.model = SentenceTransformer(self.model_name)
            print("✓ Model loaded successfully")
    
    def prepare_case_text(self, case: pd.Series) -> str:
        """
        Prepare comprehensive text representation of a case
        
        Args:
            case: Pandas Series with case data
            
        Returns:
            Combined text representation
        """
        parts = []
        
        # Add numeric features
        if 'income' in case:
            parts.append(f"Monthly income PKR {case['income']}")
        
        if 'family_members' in case:
            parts.append(f"Family of {case['family_members']} members")
        
        # Add text features
        if 'enquiry_feedback' in case and pd.notna(case['enquiry_feedback']):
            parts.append(str(case['enquiry_feedback']))
        
        if 'verification_notes' in case and pd.notna(case['verification_notes']):
            parts.append(str(case['verification_notes']))
        
        if 'decision_officer_comment' in case and pd.notna(case['decision_officer_comment']):
            parts.append(str(case['decision_officer_comment']))
        
        return " | ".join(parts)
    
    def train(self, historical_data: pd.DataFrame):
        """
        Train the engine on historical data
        
        Args:
            historical_data: DataFrame with historical cases
        """
        print("\n🎓 Training AI Engine on historical data...")
        print(f"   Total cases: {len(historical_data)}")
        
        self.load_model()
        self.historical_data = historical_data.copy()
        
        # Prepare text representations
        print("📝 Preparing case representations...")
        case_texts = []
        for idx, case in tqdm(historical_data.iterrows(), total=len(historical_data), desc="Processing cases"):
            case_texts.append(self.prepare_case_text(case))
        
        # Generate embeddings
        print("🧠 Generating semantic embeddings...")
        self.embeddings = self.model.encode(case_texts, show_progress_bar=True, batch_size=32)
        
        self.is_trained = True
        print(f"✓ Training complete! Engine ready with {len(historical_data)} cases")
        print(f"   Embedding dimension: {self.embeddings.shape[1]}")
    
    def predict(self, new_case: Dict, top_k: int = 20) -> Dict:
        """
        Predict decision for a new case with explanation
        
        Args:
            new_case: Dictionary with case information
            top_k: Number of similar cases to consider
            
        Returns:
            Dictionary with prediction and explanation
        """
        if not self.is_trained:
            raise ValueError("Engine not trained! Call train() first.")
        
        # Prepare new case text
        case_series = pd.Series(new_case)
        new_case_text = self.prepare_case_text(case_series)
        
        # Generate embedding for new case
        new_embedding = self.model.encode([new_case_text])
        
        # Calculate similarities
        similarities = cosine_similarity(new_embedding, self.embeddings)[0]
        
        # Get top K similar cases
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        top_similarities = similarities[top_indices]
        similar_cases = self.historical_data.iloc[top_indices].copy()
        similar_cases['similarity_score'] = top_similarities
        
        # Count decisions
        approved_count = len(similar_cases[similar_cases['final_decision'] == 'Approved'])
        rejected_count = len(similar_cases[similar_cases['final_decision'] == 'Rejected'])
        
        # Make recommendation
        recommendation = "APPROVED" if approved_count > rejected_count else "REJECTED"
        confidence = max(approved_count, rejected_count) / top_k
        
        # Generate explanation
        explanation = self._generate_explanation(
            new_case, similar_cases, approved_count, rejected_count, confidence
        )
        
        # Prepare result
        result = {
            'ai_recommendation': recommendation,
            'confidence': round(confidence, 2),
            'explanation': explanation,
            'similar_cases_count': top_k,
            'approved_matches': approved_count,
            'rejected_matches': rejected_count,
            'top_similar_cases': similar_cases.to_dict('records'),
            'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        return result
    
    def _generate_explanation(self, new_case: Dict, similar_cases: pd.DataFrame, 
                            approved_count: int, rejected_count: int, 
                            confidence: float) -> str:
        """
        Generate detailed human-readable explanation
        
        Args:
            new_case: The new case data
            similar_cases: Similar historical cases
            approved_count: Number of approved similar cases
            rejected_count: Number of rejected similar cases
            confidence: Confidence score
            
        Returns:
            Explanation string
        """
        lines = []
        
        # Summary
        total = approved_count + rejected_count
        lines.append(f"Based on analysis of {total} most similar historical cases:")
        lines.append(f"• {approved_count} cases were APPROVED ({approved_count/total*100:.0f}%)")
        lines.append(f"• {rejected_count} cases were REJECTED ({rejected_count/total*100:.0f}%)")
        lines.append(f"• Confidence Level: {confidence*100:.0f}%\n")
        
        # Case characteristics
        income = new_case.get('income', 0)
        family = new_case.get('family_members', 0)
        
        lines.append("📋 Current Case Profile:")
        lines.append(f"• Monthly Income: PKR {income:,}")
        lines.append(f"• Family Members: {family}")
        
        # Income analysis
        similar_incomes = similar_cases['income'].values
        avg_income = np.mean(similar_incomes)
        lines.append(f"• Average income in similar cases: PKR {avg_income:,.0f}\n")
        
        # Pattern analysis
        lines.append("🔍 Key Patterns from Similar Cases:")
        
        # Analyze approved cases
        if approved_count > 0:
            approved_cases = similar_cases[similar_cases['final_decision'] == 'Approved']
            avg_approved_income = approved_cases['income'].mean()
            common_comments = approved_cases['decision_officer_comment'].value_counts().head(3)
            
            lines.append(f"\n✅ Approved Cases ({approved_count}):")
            lines.append(f"   • Average income: PKR {avg_approved_income:,.0f}")
            if len(common_comments) > 0:
                lines.append(f"   • Common reasons:")
                for comment, count in common_comments.items():
                    lines.append(f"     - \"{comment}\" ({count} cases)")
        
        # Analyze rejected cases
        if rejected_count > 0:
            rejected_cases = similar_cases[similar_cases['final_decision'] == 'Rejected']
            avg_rejected_income = rejected_cases['income'].mean()
            common_comments = rejected_cases['decision_officer_comment'].value_counts().head(3)
            
            lines.append(f"\n❌ Rejected Cases ({rejected_count}):")
            lines.append(f"   • Average income: PKR {avg_rejected_income:,.0f}")
            if len(common_comments) > 0:
                lines.append(f"   • Common reasons:")
                for comment, count in common_comments.items():
                    lines.append(f"     - \"{comment}\" ({count} cases)")
        
        # Recommendation
        lines.append(f"\n💡 AI Recommendation: {('APPROVE' if approved_count > rejected_count else 'REJECT')} this case")
        
        return "\n".join(lines)
    
    def save(self, save_dir: str = 'engine/model_cache'):
        """
        Save trained engine to disk
        
        Args:
            save_dir: Directory to save the model
        """
        if not self.is_trained:
            raise ValueError("Cannot save untrained engine")
        
        os.makedirs(save_dir, exist_ok=True)
        
        print(f"\n💾 Saving AI engine to {save_dir}...")
        
        # Save embeddings
        embeddings_path = os.path.join(save_dir, 'embeddings.npy')
        np.save(embeddings_path, self.embeddings)
        print(f"✓ Saved embeddings: {embeddings_path}")
        
        # Save historical data and metadata
        engine_data = {
            'historical_data': self.historical_data,
            'model_name': self.model_name,
            'is_trained': self.is_trained
        }
        engine_path = os.path.join(save_dir, 'welfare_ai_engine.pkl')
        joblib.dump(engine_data, engine_path)
        print(f"✓ Saved engine data: {engine_path}")
        
        print("✓ AI Engine saved successfully!")
    
    def load(self, save_dir: str = 'engine/model_cache'):
        """
        Load trained engine from disk
        
        Args:
            save_dir: Directory to load from
        """
        print(f"\n📂 Loading AI engine from {save_dir}...")
        
        # Load embeddings
        embeddings_path = os.path.join(save_dir, 'embeddings.npy')
        if not os.path.exists(embeddings_path):
            raise FileNotFoundError(f"Embeddings not found at {embeddings_path}")
        
        self.embeddings = np.load(embeddings_path)
        print(f"✓ Loaded embeddings: {self.embeddings.shape}")
        
        # Load engine data
        engine_path = os.path.join(save_dir, 'welfare_ai_engine.pkl')
        if not os.path.exists(engine_path):
            raise FileNotFoundError(f"Engine data not found at {engine_path}")
        
        engine_data = joblib.load(engine_path)
        self.historical_data = engine_data['historical_data']
        self.model_name = engine_data['model_name']
        self.is_trained = engine_data['is_trained']
        
        # Load the transformer model
        self.load_model()
        
        print(f"✓ AI Engine loaded successfully!")
        print(f"   Total historical cases: {len(self.historical_data)}")
