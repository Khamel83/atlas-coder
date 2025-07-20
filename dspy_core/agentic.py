"""
Agentic Work Detection and Management for Atlas Coder v6
Intelligent autonomous operation with meaningful work detection
"""

import os
import time
import json
import subprocess
import threading
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum

import dspy
from .signatures import *
from .optimization import get_cost_tracker
from .progressive_execution import get_progressive_executor

class WorkPriority(Enum):
    """Work priority levels"""
    URGENT = "urgent"          # Immediate attention needed
    HIGH = "high"              # Important but not urgent
    MEDIUM = "medium"          # Normal priority
    LOW = "low"                # Background tasks
    MAINTENANCE = "maintenance" # System maintenance

class WorkType(Enum):
    """Types of work Atlas Coder can perform"""
    BUG_FIX = "bug_fix"
    CODE_REVIEW = "code_review"
    OPTIMIZATION = "optimization"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    REFACTORING = "refactoring"
    SECURITY_AUDIT = "security_audit"
    DEPENDENCY_UPDATE = "dependency_update"
    PERFORMANCE_ANALYSIS = "performance_analysis"

@dataclass
class WorkItem:
    """Represents a unit of work to be done"""
    id: str
    type: WorkType
    priority: WorkPriority
    description: str
    context: Dict[str, Any]
    estimated_effort: float  # In minutes
    estimated_cost: float    # In dollars
    value_score: float       # Expected value (0.0 to 1.0)
    deadline: Optional[datetime]
    dependencies: List[str]  # Other work item IDs
    created_at: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        # Convert datetime objects to ISO strings
        data['created_at'] = self.created_at.isoformat()
        if self.deadline:
            data['deadline'] = self.deadline.isoformat()
        # Convert enums to strings
        data['type'] = self.type.value
        data['priority'] = self.priority.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WorkItem':
        """Create from dictionary"""
        # Convert strings back to datetime objects
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        if data.get('deadline'):
            data['deadline'] = datetime.fromisoformat(data['deadline'])
        else:
            data['deadline'] = None
        # Convert strings back to enums
        data['type'] = WorkType(data['type'])
        data['priority'] = WorkPriority(data['priority'])
        return cls(**data)

# Agentic signatures for work detection and analysis
class DetectMeaningfulWork(dspy.Signature):
    """Detect meaningful work opportunities from project state"""
    project_state = dspy.InputField(desc="Current state of the project including files, git status, issues")
    recent_changes = dspy.InputField(desc="Recent changes and modifications to the project")
    context = dspy.InputField(desc="Additional context about project goals and priorities")
    work_opportunities = dspy.OutputField(desc="List of meaningful work opportunities with descriptions")
    priority_assessment = dspy.OutputField(desc="Priority assessment for each opportunity")
    value_estimation = dspy.OutputField(desc="Estimated value and impact of each opportunity")

class AssessWorkValue(dspy.Signature):
    """Assess the value and priority of potential work"""
    work_description = dspy.InputField(desc="Description of the potential work to be done")
    project_context = dspy.InputField(desc="Current project context and goals")
    resource_constraints = dspy.InputField(desc="Available resources and constraints")
    value_score = dspy.OutputField(desc="Value score from 0.0 to 1.0 based on impact and importance")
    effort_estimate = dspy.OutputField(desc="Estimated effort required in minutes")
    cost_estimate = dspy.OutputField(desc="Estimated cost in dollars")
    urgency_level = dspy.OutputField(desc="Urgency level: urgent, high, medium, low, maintenance")

class PlanWorkSequence(dspy.Signature):
    """Plan optimal sequence for executing multiple work items"""
    work_items = dspy.InputField(desc="List of work items to be sequenced")
    constraints = dspy.InputField(desc="Time, budget, and dependency constraints")
    goals = dspy.InputField(desc="Primary goals and success criteria")
    execution_plan = dspy.OutputField(desc="Optimal sequence and timing for work execution")
    resource_allocation = dspy.OutputField(desc="Resource allocation strategy")
    risk_mitigation = dspy.OutputField(desc="Risk assessment and mitigation strategies")

class AgenticWorkManager:
    """Detect meaningful work and manage continuous operation efficiently"""
    
    def __init__(self, project_root: str = ".", daily_budget: float = 3.0):
        self.project_root = Path(project_root)
        self.daily_budget = daily_budget
        self.cost_tracker = get_cost_tracker()
        self.executor = get_progressive_executor()
        
        # Work detection modules
        self.work_detector = dspy.ChainOfThought(DetectMeaningfulWork)
        self.value_assessor = dspy.ChainOfThought(AssessWorkValue)
        self.work_planner = dspy.ChainOfThought(PlanWorkSequence)
        
        # State management
        self.work_queue: List[WorkItem] = []
        self.completed_work: List[WorkItem] = []
        self.active_work: Optional[WorkItem] = None
        
        # Configuration
        self.min_value_threshold = 0.3  # Minimum value score to consider work
        self.max_work_queue_size = 20
        self.scan_interval = 300  # 5 minutes between scans
        self.cost_threshold_per_task = 0.05  # 5 cents max per task
        
        # State files
        self.state_dir = self.project_root / ".atlas_coder"
        self.state_dir.mkdir(exist_ok=True)
        self.work_queue_file = self.state_dir / "work_queue.json"
        self.completed_work_file = self.state_dir / "completed_work.json"
        
        self._load_state()
    
    def detect_work_opportunities(self) -> List[WorkItem]:
        """Scan project for meaningful work opportunities"""
        print("🔍 Scanning for work opportunities...")
        
        try:
            # Gather project state
            project_state = self._analyze_project_state()
            recent_changes = self._get_recent_changes()
            context = self._get_project_context()
            
            # Detect opportunities using DSPy
            detection = self.work_detector(
                project_state=project_state,
                recent_changes=recent_changes,
                context=context
            )
            
            # Parse and create work items
            opportunities = self._parse_work_opportunities(
                detection.work_opportunities,
                detection.priority_assessment,
                detection.value_estimation
            )
            
            print(f"📋 Found {len(opportunities)} work opportunities")
            return opportunities
            
        except Exception as e:
            print(f"⚠️ Work detection failed: {e}")
            return []
    
    def assess_work_value(self, work_description: str, work_type: WorkType) -> Tuple[float, float, float, WorkPriority]:
        """Assess value, effort, cost, and priority for work"""
        try:
            project_context = self._get_project_context()
            remaining_budget = self.cost_tracker.get_remaining_budget()
            
            assessment = self.value_assessor(
                work_description=work_description,
                project_context=project_context,
                resource_constraints=f"Budget remaining: ${remaining_budget:.2f}, Daily limit: ${self.daily_budget}"
            )
            
            # Parse outputs
            value_score = float(assessment.value_score.split()[0]) if assessment.value_score else 0.5
            effort_minutes = self._parse_effort(assessment.effort_estimate)
            cost_dollars = self._parse_cost(assessment.cost_estimate)
            priority = self._parse_priority(assessment.urgency_level)
            
            return value_score, effort_minutes, cost_dollars, priority
            
        except Exception as e:
            print(f"⚠️ Work assessment failed: {e}")
            # Default conservative values
            return 0.3, 30.0, 0.02, WorkPriority.MEDIUM
    
    def should_work_now(self) -> bool:
        """Determine if there's valuable work to do right now"""
        # Check budget constraints
        remaining_budget = self.cost_tracker.get_remaining_budget()
        if remaining_budget < self.cost_threshold_per_task:
            print(f"💰 Insufficient budget remaining: ${remaining_budget:.3f}")
            return False
        
        # Check if there's high-value work in queue
        high_value_work = [w for w in self.work_queue 
                          if w.value_score > self.min_value_threshold 
                          and w.estimated_cost <= remaining_budget]
        
        if not high_value_work:
            print("📭 No high-value work available")
            return False
        
        # Check if we're not already working
        if self.active_work:
            print(f"⚡ Already working on: {self.active_work.description}")
            return False
        
        return True
    
    def get_next_work_item(self) -> Optional[WorkItem]:
        """Get the next highest-value work item"""
        if not self.work_queue:
            return None
        
        # Filter by budget and dependencies
        remaining_budget = self.cost_tracker.get_remaining_budget()
        available_work = [
            w for w in self.work_queue
            if w.estimated_cost <= remaining_budget
            and self._dependencies_satisfied(w)
        ]
        
        if not available_work:
            return None
        
        # Sort by value score and priority
        priority_weights = {
            WorkPriority.URGENT: 1000,
            WorkPriority.HIGH: 100,
            WorkPriority.MEDIUM: 10,
            WorkPriority.LOW: 1,
            WorkPriority.MAINTENANCE: 0.1
        }
        
        def score_work(work: WorkItem) -> float:
            priority_weight = priority_weights.get(work.priority, 1)
            return work.value_score * priority_weight
        
        return max(available_work, key=score_work)
    
    def execute_work_item(self, work: WorkItem) -> Dict[str, Any]:
        """Execute a work item using appropriate workflow"""
        print(f"🚀 Executing work: {work.description}")
        self.active_work = work
        
        try:
            # Map work type to workflow
            workflow_mapping = {
                WorkType.BUG_FIX: 'bug_fix',
                WorkType.CODE_REVIEW: 'analyze',
                WorkType.OPTIMIZATION: 'refactor',
                WorkType.DOCUMENTATION: 'analyze',  # Will generate docs
                WorkType.TESTING: 'generate',       # Will generate tests
                WorkType.REFACTORING: 'refactor',
                WorkType.SECURITY_AUDIT: 'analyze',
                WorkType.PERFORMANCE_ANALYSIS: 'analyze'
            }
            
            workflow_type = workflow_mapping.get(work.type, 'analyze')
            
            # Execute using progressive executor
            result = self.executor.execute_with_escalation(
                workflow_type,
                work.context,
                None  # Let it choose initial level
            )
            
            # Mark as completed
            work.completed_at = datetime.now()
            self.completed_work.append(work)
            self.work_queue.remove(work)
            self.active_work = None
            
            self._save_state()
            
            print(f"✅ Completed work: {work.description}")
            return {
                'success': result.success,
                'work_item': work,
                'result': result.result,
                'cost': result.cost,
                'quality': result.quality_score
            }
            
        except Exception as e:
            print(f"❌ Work execution failed: {e}")
            self.active_work = None
            return {
                'success': False,
                'work_item': work,
                'error': str(e)
            }
    
    def run_continuous_agent(self, max_iterations: int = 100):
        """Run continuous agentic operation"""
        print("🤖 Starting continuous agentic operation")
        
        iteration = 0
        last_scan = 0
        
        while iteration < max_iterations:
            current_time = time.time()
            
            # Periodic work detection
            if current_time - last_scan > self.scan_interval:
                opportunities = self.detect_work_opportunities()
                for opp in opportunities:
                    if len(self.work_queue) < self.max_work_queue_size:
                        self.work_queue.append(opp)
                
                last_scan = current_time
                self._save_state()
            
            # Execute work if valuable work is available
            if self.should_work_now():
                work_item = self.get_next_work_item()
                if work_item:
                    self.execute_work_item(work_item)
                else:
                    print("📝 No suitable work items found")
            
            # Check budget status
            remaining_budget = self.cost_tracker.get_remaining_budget()
            if remaining_budget <= 0:
                print("💰 Daily budget exhausted, stopping agent")
                break
            
            # Sleep before next iteration
            time.sleep(60)  # 1 minute between checks
            iteration += 1
        
        print(f"🏁 Agent completed {iteration} iterations")
    
    def _analyze_project_state(self) -> str:
        """Analyze current project state"""
        state_info = []
        
        # Git status
        try:
            git_status = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=10
            )
            if git_status.returncode == 0:
                state_info.append(f"Git status: {git_status.stdout}")
        except:
            state_info.append("Git status: Unable to determine")
        
        # File structure
        try:
            important_files = []
            for pattern in ['*.py', '*.js', '*.ts', '*.md', '*.txt']:
                important_files.extend(self.project_root.glob(pattern))
            
            state_info.append(f"Files: {[f.name for f in important_files[:10]]}")
        except:
            state_info.append("Files: Unable to scan")
        
        # Recent errors if available
        error_log = self.project_root / "last_error.log"
        if error_log.exists():
            try:
                with open(error_log, 'r') as f:
                    error_content = f.read()[-500:]  # Last 500 chars
                state_info.append(f"Recent errors: {error_content}")
            except:
                pass
        
        return '\n'.join(state_info)
    
    def _get_recent_changes(self) -> str:
        """Get recent changes to the project"""
        try:
            # Git log for recent commits
            git_log = subprocess.run(
                ['git', 'log', '--oneline', '-5'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=10
            )
            if git_log.returncode == 0:
                return f"Recent commits:\n{git_log.stdout}"
        except:
            pass
        
        return "No recent changes detected"
    
    def _get_project_context(self) -> str:
        """Get project context and goals"""
        context_sources = []
        
        # README
        readme_files = list(self.project_root.glob("README*"))
        if readme_files:
            try:
                with open(readme_files[0], 'r') as f:
                    readme_content = f.read()[:1000]  # First 1000 chars
                context_sources.append(f"README: {readme_content}")
            except:
                pass
        
        # CLAUDE.md if it exists
        claude_md = self.project_root / "CLAUDE.md"
        if claude_md.exists():
            try:
                with open(claude_md, 'r') as f:
                    claude_content = f.read()[:500]
                context_sources.append(f"CLAUDE.md: {claude_content}")
            except:
                pass
        
        if not context_sources:
            context_sources.append("Project context: Atlas Coder DSPy development")
        
        return '\n'.join(context_sources)
    
    def _parse_work_opportunities(self, 
                                opportunities: str,
                                priorities: str, 
                                values: str) -> List[WorkItem]:
        """Parse DSPy output into work items"""
        work_items = []
        
        try:
            # Simple parsing - in real implementation would be more sophisticated
            opp_lines = opportunities.split('\n')
            
            for i, line in enumerate(opp_lines):
                if line.strip() and not line.startswith('-'):
                    continue
                
                # Create work item
                work_id = f"work_{int(time.time())}_{i}"
                description = line.strip('- ').strip()
                
                if len(description) < 10:  # Skip very short descriptions
                    continue
                
                # Assess this opportunity
                value_score, effort, cost, priority = self.assess_work_value(
                    description, WorkType.CODE_REVIEW  # Default type
                )
                
                if value_score >= self.min_value_threshold:
                    work_item = WorkItem(
                        id=work_id,
                        type=WorkType.CODE_REVIEW,
                        priority=priority,
                        description=description,
                        context={'description': description},
                        estimated_effort=effort,
                        estimated_cost=cost,
                        value_score=value_score,
                        deadline=None,
                        dependencies=[],
                        created_at=datetime.now()
                    )
                    work_items.append(work_item)
        
        except Exception as e:
            print(f"⚠️ Failed to parse work opportunities: {e}")
        
        return work_items
    
    def _parse_effort(self, effort_str: str) -> float:
        """Parse effort estimate from string"""
        try:
            # Extract numbers from string
            import re
            numbers = re.findall(r'\d+', effort_str)
            if numbers:
                return float(numbers[0])
        except:
            pass
        return 30.0  # Default 30 minutes
    
    def _parse_cost(self, cost_str: str) -> float:
        """Parse cost estimate from string"""
        try:
            import re
            # Look for dollar amounts
            dollar_match = re.search(r'\$?(\d+\.?\d*)', cost_str)
            if dollar_match:
                return float(dollar_match.group(1))
        except:
            pass
        return 0.02  # Default 2 cents
    
    def _parse_priority(self, priority_str: str) -> WorkPriority:
        """Parse priority from string"""
        priority_str = priority_str.lower()
        if 'urgent' in priority_str:
            return WorkPriority.URGENT
        elif 'high' in priority_str:
            return WorkPriority.HIGH
        elif 'low' in priority_str:
            return WorkPriority.LOW
        elif 'maintenance' in priority_str:
            return WorkPriority.MAINTENANCE
        else:
            return WorkPriority.MEDIUM
    
    def _dependencies_satisfied(self, work: WorkItem) -> bool:
        """Check if work dependencies are satisfied"""
        if not work.dependencies:
            return True
        
        completed_ids = {w.id for w in self.completed_work}
        return all(dep_id in completed_ids for dep_id in work.dependencies)
    
    def _load_state(self):
        """Load work queue and completed work from disk"""
        try:
            if self.work_queue_file.exists():
                with open(self.work_queue_file, 'r') as f:
                    queue_data = json.load(f)
                    self.work_queue = [WorkItem.from_dict(item) for item in queue_data]
            
            if self.completed_work_file.exists():
                with open(self.completed_work_file, 'r') as f:
                    completed_data = json.load(f)
                    self.completed_work = [WorkItem.from_dict(item) for item in completed_data]
                    
        except Exception as e:
            print(f"⚠️ State load failed: {e}")
    
    def _save_state(self):
        """Save work queue and completed work to disk"""
        try:
            with open(self.work_queue_file, 'w') as f:
                queue_data = [item.to_dict() for item in self.work_queue]
                json.dump(queue_data, f, indent=2)
            
            with open(self.completed_work_file, 'w') as f:
                completed_data = [item.to_dict() for item in self.completed_work]
                json.dump(completed_data, f, indent=2)
                
        except Exception as e:
            print(f"⚠️ State save failed: {e}")
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            'work_queue_size': len(self.work_queue),
            'completed_work_count': len(self.completed_work),
            'active_work': self.active_work.description if self.active_work else None,
            'remaining_budget': self.cost_tracker.get_remaining_budget(),
            'high_value_work_available': len([w for w in self.work_queue if w.value_score > self.min_value_threshold]),
            'next_scan_in': max(0, self.scan_interval - (time.time() % self.scan_interval))
        }

# Convenience functions
def start_agent(project_root: str = ".", max_iterations: int = 100):
    """Start agentic operation"""
    manager = AgenticWorkManager(project_root)
    manager.run_continuous_agent(max_iterations)

def scan_for_work(project_root: str = ".") -> List[WorkItem]:
    """Scan for work opportunities"""
    manager = AgenticWorkManager(project_root)
    return manager.detect_work_opportunities()

def get_agent_status(project_root: str = ".") -> Dict[str, Any]:
    """Get agent status"""
    manager = AgenticWorkManager(project_root)
    return manager.get_agent_status()

# Global instance
_agentic_manager = None

def get_agentic_manager() -> AgenticWorkManager:
    """Get global agentic work manager"""
    global _agentic_manager
    if _agentic_manager is None:
        _agentic_manager = AgenticWorkManager()
    return _agentic_manager