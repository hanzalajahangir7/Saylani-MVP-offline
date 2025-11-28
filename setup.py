from setuptools import setup, find_packages

setup(
    name="saylani-ai-decision-engine",
    version="1.0.0",
    description="AI Decision Support System for Saylani Welfare Management",
    author="Saylani Welfare Trust",
    packages=find_packages(),
    install_requires=[
        'pandas>=1.5.0',
        'numpy>=1.23.0',
        'scikit-learn>=1.2.0',
        'sentence-transformers>=2.2.0',
        'streamlit>=1.28.0',
        'plotly>=5.17.0',
        'joblib>=1.3.0',
        'tqdm>=4.65.0',
        'torch>=2.0.0',
    ],
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
