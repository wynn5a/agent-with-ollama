#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qwen Model Wrapper for Smolagents

This wrapper filters out thinking tags from Qwen3 responses to make them
compatible with smolagents' code parsing.
"""

import re
from smolagents import LiteLLMModel
from typing import List, Dict, Any, Optional

class QwenModelWrapper(LiteLLMModel):
    """
    A wrapper around LiteLLMModel that filters out Qwen3's thinking tags
    to make responses compatible with smolagents.
    """
    
    def __init__(self, **kwargs):
        """Initialize the Qwen model wrapper with thinking tag filtering."""
        super().__init__(**kwargs)
    
    def _clean_thinking_tags(self, text: str) -> str:
        """
        Remove thinking tags and content from Qwen3 responses.
        
        Args:
            text: Raw response from Qwen3
            
        Returns:
            Cleaned text without thinking tags
        """
        if not text:
            return text
            
        # Remove <think>...</think> blocks
        text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
        
        # Remove any remaining thinking markers
        text = re.sub(r'</?think>', '', text)
        
        # Clean up extra whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = text.strip()
        
        return text
    
    def _fix_code_blocks(self, text: str) -> str:
        """
        Ensure code blocks are properly formatted for smolagents.
        
        Args:
            text: Text that may contain code blocks
            
        Returns:
            Text with properly formatted code blocks
        """
        # Fix common code block issues
        # Ensure code blocks start with ```py or ```python
        text = re.sub(r'```(?:python)?\s*\n', '```py\n', text)
        
        # Ensure code blocks end properly
        text = re.sub(r'```\s*$', '```', text, flags=re.MULTILINE)
        
        return text
    
    def generate(self, messages: List[Dict[str, Any]], **kwargs) -> Any:
        """
        Generate response with thinking tag filtering.
        
        Args:
            messages: List of message dictionaries
            **kwargs: Additional arguments for generation
            
        Returns:
            Response object with cleaned content
        """
        # Call the parent generate method
        response = super().generate(messages, **kwargs)
        
        # Clean the response content if it exists
        if hasattr(response, 'content') and response.content:
            cleaned_content = self._clean_thinking_tags(response.content)
            cleaned_content = self._fix_code_blocks(cleaned_content)
            response.content = cleaned_content
        
        return response

def create_qwen_model(
    model_id: str = "ollama_chat/qwen3:latest",
    api_base: str = "http://localhost:11434",
    api_key: str = "dummy_key",
    num_ctx: int = 8192,
    temperature: float = 0.1,
    **kwargs
) -> QwenModelWrapper:
    """
    Create a Qwen model wrapper optimized for smolagents.
    
    Args:
        model_id: Ollama model identifier
        api_base: Ollama API base URL
        api_key: API key (dummy for local Ollama)
        num_ctx: Context window size
        temperature: Sampling temperature
        **kwargs: Additional model parameters
        
    Returns:
        Configured QwenModelWrapper instance
    """
    return QwenModelWrapper(
        model_id=model_id,
        api_base=api_base,
        api_key=api_key,
        num_ctx=num_ctx,
        temperature=temperature,
        **kwargs
    ) 