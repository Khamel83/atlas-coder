"""DSPy signature definitions for Atlas Coder.

This module defines DSPy signatures for bug diagnosis, code fixing, test generation,
and other core Atlas Coder workflows.
"""


import dspy


class BugDiagnosis(dspy.Signature):
    """Diagnose bugs in code and provide analysis."""

    code: str = dspy.InputField(desc="The code with potential bugs")
    error_message: str | None = dspy.InputField(
        desc="Error message if available", default=""
    )
    context: str | None = dspy.InputField(
        desc="Additional context about the issue", default=""
    )

    diagnosis: str = dspy.OutputField(desc="Detailed analysis of the bug(s) found")
    root_cause: str = dspy.OutputField(desc="Root cause of the issue")
    severity: str = dspy.OutputField(desc="Bug severity: critical, high, medium, low")
    fix_strategy: str = dspy.OutputField(desc="High-level strategy for fixing the bug")


class CodeFix(dspy.Signature):
    """Generate fixed code based on bug diagnosis."""

    original_code: str = dspy.InputField(desc="The original code with bugs")
    diagnosis: str = dspy.InputField(desc="Bug diagnosis from BugDiagnosis")
    fix_strategy: str = dspy.InputField(desc="Strategy for fixing the bug")

    fixed_code: str = dspy.OutputField(desc="The corrected code")
    changes_made: str = dspy.OutputField(desc="Summary of changes made to fix the bug")
    explanation: str = dspy.OutputField(
        desc="Explanation of why these changes fix the issue"
    )


class TestGeneration(dspy.Signature):
    """Generate tests for fixed code to prevent regression."""

    code: str = dspy.InputField(desc="The fixed code to test")
    original_bug: str = dspy.InputField(desc="Description of the original bug")

    test_code: str = dspy.OutputField(
        desc="Complete test code with multiple test cases"
    )
    test_strategy: str = dspy.OutputField(desc="Testing strategy and rationale")
    edge_cases: str = dspy.OutputField(desc="Edge cases covered by the tests")


class CodeGeneration(dspy.Signature):
    """Generate new code from requirements."""

    requirements: str = dspy.InputField(
        desc="Detailed requirements for the code to generate"
    )
    language: str = dspy.InputField(
        desc="Programming language (Python, JavaScript, etc.)"
    )
    style: str | None = dspy.InputField(desc="Code style preferences", default="")

    code: str = dspy.OutputField(desc="Generated code that meets the requirements")
    structure: str = dspy.OutputField(
        desc="Explanation of code structure and design decisions"
    )
    usage_example: str = dspy.OutputField(
        desc="Example of how to use the generated code"
    )


class CodeAnalysis(dspy.Signature):
    """Analyze code for quality, security, and best practices."""

    code: str = dspy.InputField(desc="Code to analyze")
    focus: str | None = dspy.InputField(
        desc="Analysis focus: security, performance, style, all", default="all"
    )

    analysis: str = dspy.OutputField(desc="Comprehensive code analysis")
    issues: str = dspy.OutputField(desc="Issues found with severity levels")
    recommendations: str = dspy.OutputField(
        desc="Specific recommendations for improvement"
    )
    score: str = dspy.OutputField(desc="Overall code quality score and justification")


class RefactoringSuggestion(dspy.Signature):
    """Suggest refactoring improvements for code."""

    code: str = dspy.InputField(desc="Code to refactor")
    goals: str = dspy.InputField(
        desc="Refactoring goals: readability, performance, maintainability"
    )

    refactored_code: str = dspy.OutputField(desc="Refactored version of the code")
    improvements: str = dspy.OutputField(desc="List of improvements made")
    benefits: str = dspy.OutputField(desc="Benefits of the refactoring")
