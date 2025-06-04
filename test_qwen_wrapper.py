#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Qwen Model Wrapper

This script tests the thinking tag filtering functionality.
"""

import sys
import os

# Add utils directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from qwen_model_wrapper import QwenModelWrapper

def test_thinking_tag_removal():
    """Test the thinking tag removal functionality."""
    
    # Create a wrapper instance (we won't actually call the model)
    wrapper = QwenModelWrapper(
        model_id="ollama_chat/qwen3:latest",
        api_base="http://localhost:11434",
        api_key="dummy_key"
    )
    
    # Test cases with thinking tags
    test_cases = [
        {
            "input": "<think>Let me think about this problem...</think>\n\nThe answer is 4.",
            "expected": "The answer is 4."
        },
        {
            "input": "Here's the solution:\n<think>I need to calculate 2+2</think>\n\n```py\nresult = 2 + 2\nprint(result)\n```",
            "expected": "Here's the solution:\n\n```py\nresult = 2 + 2\nprint(result)\n```"
        },
        {
            "input": "<think>\nThis is a multi-line\nthinking block\n</think>\n\nFinal answer: 42",
            "expected": "Final answer: 42"
        }
    ]
    
    print("Testing thinking tag removal...")
    print("=" * 50)
    
    all_passed = True
    for i, test_case in enumerate(test_cases, 1):
        result = wrapper._clean_thinking_tags(test_case["input"])
        passed = result.strip() == test_case["expected"].strip()
        
        print(f"\nTest {i}: {'PASS' if passed else 'FAIL'}")
        print(f"Input: {repr(test_case['input'])}")
        print(f"Expected: {repr(test_case['expected'])}")
        print(f"Got: {repr(result)}")
        
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 50)
    print(f"Overall result: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    
    return all_passed

if __name__ == "__main__":
    test_thinking_tag_removal() 