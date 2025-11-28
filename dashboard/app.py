"""
Streamlit Dashboard for Saylani AI Decision Support System
Professional interface for decision officers
"""
import sys
import os
# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from engine.predictor import get_ai_decision_verdict, get_engine
from utils.data_preprocessor import load_historical_data, validate_data


# Page configuration
st.set_page_config(
    page_title="Saylani AI Decision Support",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin-top: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .approved {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
    }
    .rejected {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


def load_engine_and_data():
    """Load AI engine and historical data"""
    try:
        engine = get_engine()
        data_path = "Saylani_data (1)(Sheet1).csv"
        
        if os.path.exists(data_path):
            historical_data = load_historical_data(data_path)
            return engine, historical_data
        else:
            st.error(f"❌ Data file not found: {data_path}")
            return None, None
    except Exception as e:
        st.error(f"❌ Error loading engine: {e}")
        st.info("💡 Please run 'run_first_time.bat' to train the AI engine first!")
        return None, None


def render_header():
    """Render dashboard header"""
    st.markdown('<div class="main-header">🤝 Saylani AI Decision Support System</div>', unsafe_allow_html=True)
    st.markdown("---")


def render_new_case_form():
    """Render form for new applicant evaluation"""
    st.markdown('<div class="sub-header">📝 New Applicant Evaluation</div>', unsafe_allow_html=True)
    
    with st.form("new_case_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            income = st.number_input(
                "Monthly Income (PKR)",
                min_value=0,
                max_value=100000,
                value=15000,
                step=1000,
                help="Enter the applicant's monthly household income"
            )
            
            family_members = st.number_input(
                "Number of Family Members",
                min_value=1,
                max_value=20,
                value=8,
                step=1,
                help="Total number of family members"
            )
        
        with col2:
            enquiry_feedback = st.text_area(
                "Enquiry Officer Feedback",
                height=100,
                placeholder="e.g., Very poor condition, no stable income",
                help="Notes from the enquiry officer's visit"
            )
        
        verification_notes = st.text_area(
            "Verification Officer Notes",
            height=100,
            placeholder="e.g., CNIC verified, documents match",
            help="Notes from document verification"
        )
        
        decision_comment = st.text_area(
            "Decision Officer Comments",
            height=100,
            placeholder="e.g., Genuine case, needs urgent help",
            help="Your preliminary assessment"
        )
        
        submitted = st.form_submit_button("🤖 Get AI Recommendation", use_container_width=True)
        
        if submitted:
            case_data = {
                "income": income,
                "family_members": family_members,
                "enquiry_feedback": enquiry_feedback,
                "verification_notes": verification_notes,
                "decision_officer_comment": decision_comment
            }
            
            return case_data
    
    return None


def render_ai_verdict(result):
    """Render AI verdict with styling"""
    st.markdown('<div class="sub-header">🤖 AI Recommendation</div>', unsafe_allow_html=True)
    
    recommendation = result['ai_recommendation']
    confidence = result['confidence']
    
    # Display recommendation with appropriate styling
    if recommendation == "APPROVED":
        st.markdown(f"""
        <div class="approved">
            <h2>✅ RECOMMENDATION: APPROVE</h2>
            <p style="font-size: 1.2rem;">Confidence: {confidence*100:.0f}%</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="rejected">
            <h2>❌ RECOMMENDATION: REJECT</h2>
            <p style="font-size: 1.2rem;">Confidence: {confidence*100:.0f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Similar Cases Analyzed",
            result['similar_cases_count']
        )
    
    with col2:
        st.metric(
            "Approved Matches",
            result['approved_matches'],
            delta=f"{result['approved_matches']/result['similar_cases_count']*100:.0f}%"
        )
    
    with col3:
        st.metric(
            "Rejected Matches",
            result['rejected_matches'],
            delta=f"{result['rejected_matches']/result['similar_cases_count']*100:.0f}%"
        )


def render_explanation(result):
    """Render detailed explanation"""
    st.markdown('<div class="sub-header">💡 Detailed Explanation</div>', unsafe_allow_html=True)
    
    with st.expander("📊 View Full Analysis", expanded=True):
        st.text(result['explanation'])


def render_similar_cases(result):
    """Render similar cases table"""
    st.markdown('<div class="sub-header">📋 Top 10 Most Similar Historical Cases</div>', unsafe_allow_html=True)
    
    if result['top_similar_cases']:
        # Convert to DataFrame
        similar_df = pd.DataFrame(result['top_similar_cases'][:10])
        
        # Select relevant columns
        display_cols = ['case_id', 'income', 'family_members', 'final_decision', 
                       'aid_amount', 'similarity_score', 'decision_officer_comment']
        
        # Filter columns that exist
        display_cols = [col for col in display_cols if col in similar_df.columns]
        
        # Format similarity score
        if 'similarity_score' in similar_df.columns:
            similar_df['similarity_score'] = similar_df['similarity_score'].apply(lambda x: f"{x:.2%}")
        
        # Display table
        st.dataframe(
            similar_df[display_cols],
            use_container_width=True,
            hide_index=True
        )


def render_analytics(historical_data):
    """Render historical analytics"""
    st.markdown('<div class="sub-header">📊 Historical Analytics</div>', unsafe_allow_html=True)
    
    # Key metrics
    stats = validate_data(historical_data)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Cases", f"{stats['total_cases']:,}")
    
    with col2:
        st.metric("Approved", f"{stats['approved_cases']:,}", 
                 delta=f"{stats['approval_rate']:.1f}%")
    
    with col3:
        st.metric("Rejected", f"{stats['rejected_cases']:,}",
                 delta=f"{100-stats['approval_rate']:.1f}%")
    
    with col4:
        avg_income = historical_data['income'].mean()
        st.metric("Avg Income", f"PKR {avg_income:,.0f}")
    
    # Charts
    tab1, tab2, tab3 = st.tabs(["📈 Income Distribution", "👨‍👩‍👧‍👦 Family Size", "✅ Approval Trends"])
    
    with tab1:
        # Income distribution by decision
        fig = px.histogram(
            historical_data,
            x='income',
            color='final_decision',
            nbins=50,
            title='Income Distribution by Decision',
            labels={'income': 'Monthly Income (PKR)', 'count': 'Number of Cases'},
            color_discrete_map={'Approved': '#28a745', 'Rejected': '#dc3545'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Family size distribution
        family_dist = historical_data.groupby(['family_members', 'final_decision']).size().reset_index(name='count')
        fig = px.bar(
            family_dist,
            x='family_members',
            y='count',
            color='final_decision',
            title='Cases by Family Size',
            labels={'family_members': 'Number of Family Members', 'count': 'Number of Cases'},
            color_discrete_map={'Approved': '#28a745', 'Rejected': '#dc3545'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Approval rate by income bracket
        historical_data['income_bracket'] = pd.cut(
            historical_data['income'],
            bins=[0, 20000, 30000, 40000, 50000, 100000],
            labels=['<20k', '20-30k', '30-40k', '40-50k', '>50k']
        )
        
        approval_by_income = historical_data.groupby('income_bracket')['final_decision'].apply(
            lambda x: (x == 'Approved').sum() / len(x) * 100
        ).reset_index(name='approval_rate')
        
        fig = px.bar(
            approval_by_income,
            x='income_bracket',
            y='approval_rate',
            title='Approval Rate by Income Bracket',
            labels={'income_bracket': 'Income Bracket (PKR)', 'approval_rate': 'Approval Rate (%)'},
            color='approval_rate',
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig, use_container_width=True)


def main():
    """Main dashboard function"""
    render_header()
    
    # Load engine and data
    engine, historical_data = load_engine_and_data()
    
    if engine is None or historical_data is None:
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100/1f77b4/ffffff?text=Saylani+Welfare", use_container_width=True)
        st.markdown("### 🎯 System Status")
        st.success("✅ AI Engine: Active")
        st.info(f"📊 Historical Cases: {len(historical_data):,}")
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        This AI-powered system assists decision officers by:
        - Analyzing 100,000+ historical cases
        - Providing data-driven recommendations
        - Explaining decisions with similar cases
        - Running completely offline
        """)
    
    # Main content
    case_data = render_new_case_form()
    
    if case_data:
        with st.spinner("🤖 AI is analyzing the case..."):
            result = get_ai_decision_verdict(case_data)
        
        if result['ai_recommendation'] != 'ERROR':
            render_ai_verdict(result)
            render_explanation(result)
            render_similar_cases(result)
        else:
            st.error(f"❌ Error: {result['explanation']}")
    
    # Analytics section
    st.markdown("---")
    render_analytics(historical_data)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #7f8c8d; padding: 1rem;'>
        <p>🤝 Saylani Welfare AI Decision Support System | Built with ❤️ for social good</p>
        <p style='font-size: 0.8rem;'>Powered by Sentence Transformers | 100% Offline & Private</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
