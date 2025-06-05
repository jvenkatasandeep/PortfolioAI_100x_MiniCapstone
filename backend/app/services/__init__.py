"""
Services package for the PortfolioAI backend.
"""

from backend.services.resume_parser import extract_text_from_pdf, extract_text_from_docx, extract_text_from_file
from backend.services.portfolio_builder import PortfolioBuilder, portfolio_builder
from backend.services.groq_client import GroqClient
from backend.services.cv_generator import CVGenerator, cv_generator
from backend.services.optimizer import ResumeOptimizer, resume_optimizer

__all__ = [
    # Resume Parser
    'extract_text_from_pdf',
    'extract_text_from_docx',
    'extract_text_from_file',
    
    # Portfolio Builder
    'PortfolioBuilder',
    'portfolio_builder',
    
    # Groq Client
    'GroqClient',
    
    # CV Generator
    'CVGenerator',
    'cv_generator',
    
    # Resume Optimizer
    'ResumeOptimizer',
    'resume_optimizer'
]