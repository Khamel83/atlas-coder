"""
Core DSPy Signature Library for Atlas Coder
Revolutionary programming approach - no prompts, only systematic behaviors
"""

import dspy

# === CODE ANALYSIS SIGNATURES ===
class AnalyzeCode(dspy.Signature):
    """Systematic code analysis and understanding"""
    code = dspy.InputField(desc="Source code to analyze")
    analysis = dspy.OutputField(desc="Detailed technical analysis of code structure, patterns, and quality")
    issues = dspy.OutputField(desc="List of potential problems, bugs, or improvements")
    architecture = dspy.OutputField(desc="High-level architectural assessment and design patterns used")

class UnderstandRequirements(dspy.Signature):
    """Convert natural language requirements into structured technical specifications"""
    requirements = dspy.InputField(desc="Natural language description of what needs to be built")
    understanding = dspy.OutputField(desc="Structured technical understanding with clear scope and constraints")
    specifications = dspy.OutputField(desc="Detailed technical specifications and acceptance criteria")
    architecture_plan = dspy.OutputField(desc="Proposed system architecture and technology choices")

# === CODE GENERATION SIGNATURES ===
class GenerateCode(dspy.Signature):
    """Generate production-ready code from specifications"""
    specifications = dspy.InputField(desc="Technical specifications and requirements")
    understanding = dspy.InputField(desc="Contextual understanding of the system")
    code = dspy.OutputField(desc="Complete, production-ready code implementation")
    explanation = dspy.OutputField(desc="Clear explanation of implementation choices and patterns used")

class GenerateTests(dspy.Signature):
    """Generate comprehensive test suites for code"""
    code = dspy.InputField(desc="Source code to test")
    requirements = dspy.InputField(desc="Original requirements and expected behavior")
    tests = dspy.OutputField(desc="Complete test suite with unit, integration, and edge case tests")
    coverage_plan = dspy.OutputField(desc="Test coverage strategy and areas of focus")

# === BUG FIXING SIGNATURES ===
class DiagnoseBug(dspy.Signature):
    """Systematic bug diagnosis and root cause analysis"""
    code = dspy.InputField(desc="Code containing the bug")
    error = dspy.InputField(desc="Error message, traceback, or description of unexpected behavior")
    context = dspy.InputField(desc="Additional context about when/how the bug occurs")
    diagnosis = dspy.OutputField(desc="Root cause analysis and technical diagnosis")
    impact_assessment = dspy.OutputField(desc="Assessment of bug impact and severity")
    reproduction_steps = dspy.OutputField(desc="Clear steps to reproduce the issue")

class FixBug(dspy.Signature):
    """Generate bug fixes with validation"""
    code = dspy.InputField(desc="Original code with bug")
    diagnosis = dspy.InputField(desc="Bug diagnosis and root cause analysis")
    error = dspy.InputField(desc="Error details and expected behavior")
    fixed_code = dspy.OutputField(desc="Corrected code with bug resolved")
    fix_explanation = dspy.OutputField(desc="Explanation of what was changed and why")
    validation_tests = dspy.OutputField(desc="Tests to verify the fix works correctly")

# === CODE QUALITY SIGNATURES ===
class ReviewCode(dspy.Signature):
    """Comprehensive code review and quality assessment"""
    code = dspy.InputField(desc="Code to review")
    requirements = dspy.InputField(desc="Original requirements and context")
    review = dspy.OutputField(desc="Detailed code review with quality assessment")
    suggestions = dspy.OutputField(desc="Specific improvement suggestions with rationale")
    security_analysis = dspy.OutputField(desc="Security vulnerabilities and recommendations")

class RefactorCode(dspy.Signature):
    """Systematic code refactoring for improvement"""
    code = dspy.InputField(desc="Code to refactor")
    goals = dspy.InputField(desc="Refactoring goals (performance, readability, maintainability)")
    refactored_code = dspy.OutputField(desc="Improved code maintaining identical functionality")
    improvements = dspy.OutputField(desc="List of improvements made and their benefits")
    migration_guide = dspy.OutputField(desc="Guide for safely migrating from old to new code")

# === DOCUMENTATION SIGNATURES ===
class GenerateDocumentation(dspy.Signature):
    """Generate comprehensive project documentation"""
    code = dspy.InputField(desc="Source code to document")
    architecture = dspy.InputField(desc="System architecture and design decisions")
    requirements = dspy.InputField(desc="Original requirements and functionality")
    documentation = dspy.OutputField(desc="Complete documentation including API docs, guides, and examples")
    examples = dspy.OutputField(desc="Working code examples demonstrating key functionality")
    deployment_guide = dspy.OutputField(desc="Setup and deployment instructions")

class GenerateREADME(dspy.Signature):
    """Generate professional README files"""
    project_info = dspy.InputField(desc="Project name, description, and key features")
    code_analysis = dspy.InputField(desc="Analysis of project structure and functionality")
    setup_requirements = dspy.InputField(desc="Dependencies and setup requirements")
    readme = dspy.OutputField(desc="Professional README with clear structure and examples")
    badges = dspy.OutputField(desc="Relevant project badges and status indicators")

# === ARCHITECTURE SIGNATURES ===
class DesignArchitecture(dspy.Signature):
    """Design system architecture from requirements"""
    requirements = dspy.InputField(desc="Functional and non-functional requirements")
    constraints = dspy.InputField(desc="Technical constraints and limitations")
    architecture = dspy.OutputField(desc="Complete system architecture design")
    technology_choices = dspy.OutputField(desc="Recommended technologies with justification")
    scalability_plan = dspy.OutputField(desc="Scalability considerations and growth strategy")

class OptimizePerformance(dspy.Signature):
    """Analyze and optimize code performance"""
    code = dspy.InputField(desc="Code to optimize")
    performance_goals = dspy.InputField(desc="Performance targets and constraints")
    bottlenecks = dspy.OutputField(desc="Identified performance bottlenecks and issues")
    optimized_code = dspy.OutputField(desc="Performance-optimized code")
    benchmarks = dspy.OutputField(desc="Performance benchmarks and measurement strategy")

# === SECURITY SIGNATURES ===
class SecurityAudit(dspy.Signature):
    """Comprehensive security analysis"""
    code = dspy.InputField(desc="Code to audit for security issues")
    context = dspy.InputField(desc="Application context and threat model")
    vulnerabilities = dspy.OutputField(desc="Identified security vulnerabilities and risks")
    fixes = dspy.OutputField(desc="Specific security fixes and hardening recommendations")
    compliance = dspy.OutputField(desc="Compliance considerations and standards alignment")

# === PROJECT MANAGEMENT SIGNATURES ===
class PlanProject(dspy.Signature):
    """Create comprehensive project implementation plan"""
    requirements = dspy.InputField(desc="Complete project requirements and goals")
    constraints = dspy.InputField(desc="Timeline, resource, and technical constraints")
    project_plan = dspy.OutputField(desc="Detailed project plan with phases and milestones")
    task_breakdown = dspy.OutputField(desc="Work breakdown structure with dependencies")
    risk_assessment = dspy.OutputField(desc="Risk analysis and mitigation strategies")

class EstimateComplexity(dspy.Signature):
    """Estimate development complexity and effort"""
    requirements = dspy.InputField(desc="Project or feature requirements")
    technical_scope = dspy.InputField(desc="Technical scope and architecture considerations")
    complexity_score = dspy.OutputField(desc="Complexity rating with detailed breakdown")
    effort_estimate = dspy.OutputField(desc="Development effort estimate with confidence intervals")
    dependencies = dspy.OutputField(desc="Critical dependencies and potential blockers")