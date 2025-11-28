"""
Data preprocessing utilities for Saylani AI Decision Support System
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional


def load_historical_data(file_path: str) -> pd.DataFrame:
    """
    Load historical welfare case data from CSV file
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        DataFrame with loaded data
    """
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
        print(f"✓ Loaded {len(df)} historical cases")
        return df
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        raise


def validate_data(df: pd.DataFrame) -> Dict[str, any]:
    """
    Validate data quality and return statistics
    
    Args:
        df: DataFrame to validate
        
    Returns:
        Dictionary with validation statistics
    """
    stats = {
        'total_cases': len(df),
        'approved_cases': len(df[df['final_decision'] == 'Approved']),
        'rejected_cases': len(df[df['final_decision'] == 'Rejected']),
        'missing_values': df.isnull().sum().to_dict(),
        'income_range': (df['income'].min(), df['income'].max()),
        'family_size_range': (df['family_members'].min(), df['family_members'].max())
    }
    
    stats['approval_rate'] = stats['approved_cases'] / stats['total_cases'] * 100
    
    return stats


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and prepare data for AI engine
    
    Args:
        df: Raw DataFrame
        
    Returns:
        Cleaned DataFrame
    """
    df_clean = df.copy()
    
    # Fill missing text fields with empty string
    text_fields = ['enquiry_feedback', 'verification_notes', 'decision_officer_comment']
    for field in text_fields:
        if field in df_clean.columns:
            df_clean[field] = df_clean[field].fillna('')
    
    # Fill missing numeric fields with median
    if 'income' in df_clean.columns:
        df_clean['income'] = df_clean['income'].fillna(df_clean['income'].median())
    
    if 'family_members' in df_clean.columns:
        df_clean['family_members'] = df_clean['family_members'].fillna(df_clean['family_members'].median())
    
    # Standardize decision field
    if 'final_decision' in df_clean.columns:
        df_clean['final_decision'] = df_clean['final_decision'].str.strip().str.title()
    
    return df_clean


def prepare_case_text(case_data: Dict) -> str:
    """
    Prepare comprehensive text representation of a case
    
    Args:
        case_data: Dictionary with case information
        
    Returns:
        Combined text representation
    """
    parts = []
    
    # Add income and family info
    if 'income' in case_data:
        parts.append(f"Monthly income: PKR {case_data['income']}")
    
    if 'family_members' in case_data:
        parts.append(f"Family size: {case_data['family_members']} members")
    
    # Add text feedback
    if 'enquiry_feedback' in case_data and case_data['enquiry_feedback']:
        parts.append(f"Enquiry: {case_data['enquiry_feedback']}")
    
    if 'verification_notes' in case_data and case_data['verification_notes']:
        parts.append(f"Verification: {case_data['verification_notes']}")
    
    if 'decision_officer_comment' in case_data and case_data['decision_officer_comment']:
        parts.append(f"Officer comment: {case_data['decision_officer_comment']}")
    
    return " | ".join(parts)


def get_data_summary(df: pd.DataFrame) -> str:
    """
    Get human-readable summary of the dataset
    
    Args:
        df: DataFrame to summarize
        
    Returns:
        Summary string
    """
    stats = validate_data(df)
    
    summary = f"""
    📊 Dataset Summary:
    ==================
    Total Cases: {stats['total_cases']:,}
    Approved: {stats['approved_cases']:,} ({stats['approval_rate']:.1f}%)
    Rejected: {stats['rejected_cases']:,} ({100-stats['approval_rate']:.1f}%)
    
    Income Range: PKR {stats['income_range'][0]:,} - PKR {stats['income_range'][1]:,}
    Family Size Range: {stats['family_size_range'][0]} - {stats['family_size_range'][1]} members
    """
    
    return summary
