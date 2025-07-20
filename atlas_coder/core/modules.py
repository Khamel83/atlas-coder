"""DSPy module implementations for Atlas Coder.

This module implements DSPy modules that chain signatures together for complex
workflows like bug fixing, code generation, and analysis.
"""

from typing import Any

import dspy

from .signatures import (
    BugDiagnosis,
    CodeAnalysis,
    CodeFix,
    CodeGeneration,
    RefactoringSuggestion,
    TestGeneration,
)


class BugDiagnoser(dspy.Module):
    """Module for diagnosing bugs in code."""

    def __init__(self):
        super().__init__()
        self.diagnose = dspy.ChainOfThought(BugDiagnosis)

    def forward(
        self, code: str, error_message: str = "", context: str = ""
    ) -> dspy.Prediction:
        """Diagnose bugs in the provided code."""
        return self.diagnose(code=code, error_message=error_message, context=context)


class BugFixer(dspy.Module):
    """Module for fixing bugs based on diagnosis."""

    def __init__(self):
        super().__init__()
        self.fix = dspy.ChainOfThought(CodeFix)

    def forward(
        self, original_code: str, diagnosis: str, fix_strategy: str
    ) -> dspy.Prediction:
        """Generate fixed code based on diagnosis."""
        return self.fix(
            original_code=original_code, diagnosis=diagnosis, fix_strategy=fix_strategy
        )


class TestGenerator(dspy.Module):
    """Module for generating tests for fixed code."""

    def __init__(self):
        super().__init__()
        self.generate = dspy.ChainOfThought(TestGeneration)

    def forward(self, code: str, original_bug: str) -> dspy.Prediction:
        """Generate tests for the provided code."""
        return self.generate(code=code, original_bug=original_bug)


class CompleteBugFixer(dspy.Module):
    """Complete bug fixing workflow: Diagnose → Fix → Test."""

    def __init__(self):
        super().__init__()
        self.diagnoser = BugDiagnoser()
        self.fixer = BugFixer()
        self.test_generator = TestGenerator()

    def forward(
        self,
        code: str,
        error_message: str = "",
        context: str = "",
        generate_tests: bool = True,
    ) -> dict[str, Any]:
        """Complete bug fixing workflow."""

        # Step 1: Diagnose the bug
        diagnosis_result = self.diagnoser(
            code=code, error_message=error_message, context=context
        )

        # Step 2: Fix the bug
        fix_result = self.fixer(
            original_code=code,
            diagnosis=diagnosis_result.diagnosis,
            fix_strategy=diagnosis_result.fix_strategy,
        )

        # Step 3: Generate tests (optional)
        test_result = None
        if generate_tests:
            test_result = self.test_generator(
                code=fix_result.fixed_code, original_bug=diagnosis_result.diagnosis
            )

        return {
            "diagnosis": {
                "diagnosis": diagnosis_result.diagnosis,
                "root_cause": diagnosis_result.root_cause,
                "severity": diagnosis_result.severity,
                "fix_strategy": diagnosis_result.fix_strategy,
            },
            "fix": {
                "fixed_code": fix_result.fixed_code,
                "changes_made": fix_result.changes_made,
                "explanation": fix_result.explanation,
            },
            "tests": (
                {
                    "test_code": test_result.test_code if test_result else "",
                    "test_strategy": test_result.test_strategy if test_result else "",
                    "edge_cases": test_result.edge_cases if test_result else "",
                }
                if generate_tests and test_result
                else None
            ),
            "original_code": code,
            "success": True,
        }


class CodeGenerator(dspy.Module):
    """Module for generating new code from requirements."""

    def __init__(self):
        super().__init__()
        self.generate = dspy.ChainOfThought(CodeGeneration)

    def forward(
        self, requirements: str, language: str = "Python", style: str = ""
    ) -> dspy.Prediction:
        """Generate code from requirements."""
        return self.generate(requirements=requirements, language=language, style=style)


class CodeAnalyzer(dspy.Module):
    """Module for analyzing code quality and best practices."""

    def __init__(self):
        super().__init__()
        self.analyze = dspy.ChainOfThought(CodeAnalysis)

    def forward(self, code: str, focus: str = "all") -> dspy.Prediction:
        """Analyze code for quality, security, and best practices."""
        return self.analyze(code=code, focus=focus)


class CodeRefactorer(dspy.Module):
    """Module for suggesting and implementing code refactoring."""

    def __init__(self):
        super().__init__()
        self.refactor = dspy.ChainOfThought(RefactoringSuggestion)

    def forward(
        self, code: str, goals: str = "readability, maintainability"
    ) -> dspy.Prediction:
        """Suggest refactoring improvements for code."""
        return self.refactor(code=code, goals=goals)


class ProgramOfThought(dspy.Module):
    """Advanced reasoning module for complex coding tasks."""

    def __init__(self):
        super().__init__()
        self.analyzer = CodeAnalyzer()
        self.generator = CodeGenerator()
        self.refactorer = CodeRefactorer()

    def forward(
        self,
        task: str,
        code: str | None = None,
        requirements: str | None = None,
        language: str = "Python",
    ) -> dict[str, Any]:
        """Execute program of thought for complex coding tasks."""

        results = {
            "task": task,
            "analysis": None,
            "generated_code": None,
            "refactored_code": None,
            "success": False,
        }

        try:
            # If code is provided, analyze it first
            if code:
                analysis = self.analyzer(code=code)
                results["analysis"] = {
                    "analysis": analysis.analysis,
                    "issues": analysis.issues,
                    "recommendations": analysis.recommendations,
                    "score": analysis.score,
                }

                # Refactor if needed
                if "refactor" in task.lower():
                    refactored = self.refactorer(code=code)
                    results["refactored_code"] = {
                        "refactored_code": refactored.refactored_code,
                        "improvements": refactored.improvements,
                        "benefits": refactored.benefits,
                    }

            # Generate new code if requirements provided
            if requirements:
                generated = self.generator(requirements=requirements, language=language)
                results["generated_code"] = {
                    "code": generated.code,
                    "structure": generated.structure,
                    "usage_example": generated.usage_example,
                }

            results["success"] = True

        except Exception as e:
            results["error"] = str(e)

        return results
