"""
Community Pattern Learning System for Atlas Coder v6
Learn from community usage while maintaining privacy
"""

import os
import json
import hashlib
import time
from typing import Dict, Any, List, Optional, Set
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

import dspy

# Community learning signatures
class PatternAnalysis(dspy.Signature):
    """Analyze successful interactions for reusable patterns"""
    successful_interactions = dspy.InputField(desc="Anonymized successful interactions and outcomes")
    context_type = dspy.InputField(desc="Type of context (bug_fix, code_generation, analysis, etc.)")
    usage_frequency = dspy.InputField(desc="How frequently this pattern appears")
    reusable_patterns = dspy.OutputField(desc="Identified reusable patterns and best practices")
    optimization_opportunities = dspy.OutputField(desc="Opportunities for optimization and improvement")
    generalization_potential = dspy.OutputField(desc="How well this pattern generalizes to other contexts")

class SignatureOptimization(dspy.Signature):
    """Optimize DSPy signatures based on usage patterns"""
    usage_patterns = dspy.InputField(desc="Patterns of successful signature usage")
    performance_data = dspy.InputField(desc="Performance metrics for different signature configurations")
    context_variations = dspy.InputField(desc="Different contexts where signature is used")
    improved_signatures = dspy.OutputField(desc="Optimized signature definitions")
    better_compositions = dspy.OutputField(desc="Improved module compositions")
    usage_guidelines = dspy.OutputField(desc="Guidelines for optimal signature usage")

class CommunityInsights(dspy.Signature):
    """Generate insights from community usage data"""
    aggregated_patterns = dspy.InputField(desc="Aggregated patterns from community usage")
    success_metrics = dspy.InputField(desc="Success metrics and performance data")
    common_challenges = dspy.InputField(desc="Common challenges and failure patterns")
    community_insights = dspy.OutputField(desc="Insights about effective DSPy usage patterns")
    best_practices = dspy.OutputField(desc="Community-derived best practices")
    improvement_recommendations = dspy.OutputField(desc="Recommendations for framework improvements")

@dataclass
class InteractionPattern:
    """Represents a successful interaction pattern"""
    pattern_id: str
    signature_type: str
    context_type: str
    input_pattern: str  # Anonymized pattern
    output_pattern: str  # Anonymized pattern
    success_metrics: Dict[str, float]
    usage_count: int
    created_at: datetime
    last_used: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['last_used'] = self.last_used.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'InteractionPattern':
        """Create from dictionary"""
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['last_used'] = datetime.fromisoformat(data['last_used'])
        return cls(**data)

class CommunityPatternLearning:
    """Learn from community usage while maintaining privacy"""
    
    def __init__(self, cache_dir: str = "./dspy_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        # Pattern analysis modules
        self.pattern_analyzer = dspy.ChainOfThought(PatternAnalysis)
        self.signature_optimizer = dspy.ChainOfThought(SignatureOptimization)
        self.insights_generator = dspy.ChainOfThought(CommunityInsights)
        
        # Storage
        self.local_patterns_file = self.cache_dir / "local_patterns.json"
        self.community_patterns_file = self.cache_dir / "community_patterns.json"
        self.optimization_cache_file = self.cache_dir / "optimizations.json"
        
        # Privacy settings
        self.enable_sharing = os.getenv('ATLAS_SHARE_PATTERNS', 'false').lower() == 'true'
        self.anonymization_salt = self._get_anonymization_salt()
        
        # Pattern storage
        self.local_patterns: Dict[str, InteractionPattern] = {}
        self.community_patterns: Dict[str, InteractionPattern] = {}
        self.optimization_cache: Dict[str, Any] = {}
        
        self._load_patterns()
    
    def record_successful_interaction(self, 
                                    signature_type: str,
                                    context_type: str,
                                    inputs: Dict[str, Any],
                                    outputs: Dict[str, Any],
                                    success_metrics: Dict[str, float]):
        """Record a successful interaction for pattern learning"""
        
        # Anonymize the interaction
        anonymized_input = self._anonymize_content(inputs)
        anonymized_output = self._anonymize_content(outputs)
        
        # Create pattern ID
        pattern_content = f"{signature_type}_{context_type}_{anonymized_input}_{anonymized_output}"
        pattern_id = hashlib.sha256(pattern_content.encode()).hexdigest()[:16]
        
        # Check if pattern already exists
        if pattern_id in self.local_patterns:
            # Update existing pattern
            pattern = self.local_patterns[pattern_id]
            pattern.usage_count += 1
            pattern.last_used = datetime.now()
            
            # Update success metrics (running average)
            for key, value in success_metrics.items():
                if key in pattern.success_metrics:
                    # Running average
                    pattern.success_metrics[key] = (
                        pattern.success_metrics[key] * (pattern.usage_count - 1) + value
                    ) / pattern.usage_count
                else:
                    pattern.success_metrics[key] = value
        else:
            # Create new pattern
            pattern = InteractionPattern(
                pattern_id=pattern_id,
                signature_type=signature_type,
                context_type=context_type,
                input_pattern=anonymized_input,
                output_pattern=anonymized_output,
                success_metrics=success_metrics,
                usage_count=1,
                created_at=datetime.now(),
                last_used=datetime.now()
            )
            self.local_patterns[pattern_id] = pattern
        
        self._save_patterns()
        
        # Analyze patterns if we have enough data
        if len(self.local_patterns) % 10 == 0:  # Every 10 new patterns
            self._analyze_local_patterns()
    
    def get_optimization_suggestions(self, signature_type: str) -> Dict[str, Any]:
        """Get optimization suggestions for a signature type"""
        
        # Filter patterns for this signature type
        relevant_patterns = [
            p for p in self.local_patterns.values() 
            if p.signature_type == signature_type
        ]
        
        if len(relevant_patterns) < 3:
            return {'suggestions': 'Insufficient data for optimization'}
        
        # Analyze patterns
        pattern_data = self._prepare_pattern_data(relevant_patterns)
        
        try:
            optimization = self.signature_optimizer(
                usage_patterns=pattern_data['usage_patterns'],
                performance_data=pattern_data['performance_data'],
                context_variations=pattern_data['context_variations']
            )
            
            return {
                'improved_signatures': optimization.improved_signatures,
                'better_compositions': optimization.better_compositions,
                'usage_guidelines': optimization.usage_guidelines,
                'pattern_count': len(relevant_patterns)
            }
            
        except Exception as e:
            return {'suggestions': f'Optimization analysis failed: {e}'}
    
    def analyze_community_insights(self) -> Dict[str, Any]:
        """Generate insights from community patterns"""
        
        all_patterns = list(self.local_patterns.values()) + list(self.community_patterns.values())
        
        if len(all_patterns) < 5:
            return {'insights': 'Insufficient community data'}
        
        # Aggregate patterns by type
        aggregated = self._aggregate_patterns(all_patterns)
        success_metrics = self._calculate_success_metrics(all_patterns)
        challenges = self._identify_challenges(all_patterns)
        
        try:
            insights = self.insights_generator(
                aggregated_patterns=json.dumps(aggregated),
                success_metrics=json.dumps(success_metrics),
                common_challenges=json.dumps(challenges)
            )
            
            return {
                'insights': insights.community_insights,
                'best_practices': insights.best_practices,
                'improvements': insights.improvement_recommendations,
                'pattern_count': len(all_patterns),
                'community_size': len(self.community_patterns)
            }
            
        except Exception as e:
            return {'insights': f'Community analysis failed: {e}'}
    
    def share_patterns_anonymously(self) -> Dict[str, Any]:
        """Share anonymized patterns with community (if enabled)"""
        
        if not self.enable_sharing:
            return {'shared': False, 'reason': 'Sharing disabled'}
        
        # Select high-quality patterns for sharing
        shareable_patterns = [
            p for p in self.local_patterns.values()
            if p.usage_count >= 3 and  # Used multiple times
            p.success_metrics.get('quality_score', 0) > 0.8  # High quality
        ]
        
        if not shareable_patterns:
            return {'shared': False, 'reason': 'No high-quality patterns to share'}
        
        # Further anonymize for sharing
        shared_data = []
        for pattern in shareable_patterns:
            shared_data.append({
                'signature_type': pattern.signature_type,
                'context_type': pattern.context_type,
                'input_pattern': self._double_anonymize(pattern.input_pattern),
                'output_pattern': self._double_anonymize(pattern.output_pattern),
                'success_metrics': pattern.success_metrics,
                'usage_count': min(pattern.usage_count, 10)  # Cap for privacy
            })
        
        # In real implementation, this would upload to a community repository
        # For now, we'll save to a local "shared" file
        shared_file = self.cache_dir / "shared_patterns.json"
        try:
            with open(shared_file, 'w') as f:
                json.dump(shared_data, f, indent=2)
            
            return {
                'shared': True,
                'pattern_count': len(shared_data),
                'file': str(shared_file)
            }
            
        except Exception as e:
            return {'shared': False, 'reason': f'Sharing failed: {e}'}
    
    def import_community_patterns(self, community_data: Optional[str] = None) -> Dict[str, Any]:
        """Import community patterns from shared repository"""
        
        if community_data:
            # Import from provided data
            try:
                patterns_data = json.loads(community_data)
            except:
                return {'imported': False, 'reason': 'Invalid community data'}
        else:
            # In real implementation, this would download from community repository
            # For now, check if shared patterns exist locally
            shared_file = self.cache_dir / "shared_patterns.json"
            if not shared_file.exists():
                return {'imported': False, 'reason': 'No community patterns available'}
            
            try:
                with open(shared_file, 'r') as f:
                    patterns_data = json.load(f)
            except:
                return {'imported': False, 'reason': 'Could not load community patterns'}
        
        # Import patterns
        imported_count = 0
        for pattern_data in patterns_data:
            pattern_id = f"community_{int(time.time())}_{imported_count}"
            
            community_pattern = InteractionPattern(
                pattern_id=pattern_id,
                signature_type=pattern_data['signature_type'],
                context_type=pattern_data['context_type'],
                input_pattern=pattern_data['input_pattern'],
                output_pattern=pattern_data['output_pattern'],
                success_metrics=pattern_data['success_metrics'],
                usage_count=pattern_data['usage_count'],
                created_at=datetime.now(),
                last_used=datetime.now()
            )
            
            self.community_patterns[pattern_id] = community_pattern
            imported_count += 1
        
        self._save_patterns()
        
        return {
            'imported': True,
            'pattern_count': imported_count,
            'total_community_patterns': len(self.community_patterns)
        }
    
    def get_pattern_statistics(self) -> Dict[str, Any]:
        """Get statistics about learned patterns"""
        
        local_by_type = {}
        community_by_type = {}
        
        for pattern in self.local_patterns.values():
            sig_type = pattern.signature_type
            local_by_type[sig_type] = local_by_type.get(sig_type, 0) + 1
        
        for pattern in self.community_patterns.values():
            sig_type = pattern.signature_type
            community_by_type[sig_type] = community_by_type.get(sig_type, 0) + 1
        
        return {
            'local_patterns': {
                'total': len(self.local_patterns),
                'by_type': local_by_type,
                'avg_usage': sum(p.usage_count for p in self.local_patterns.values()) / len(self.local_patterns) if self.local_patterns else 0
            },
            'community_patterns': {
                'total': len(self.community_patterns),
                'by_type': community_by_type
            },
            'sharing_enabled': self.enable_sharing,
            'total_patterns': len(self.local_patterns) + len(self.community_patterns)
        }
    
    # Private helper methods
    def _get_anonymization_salt(self) -> str:
        """Get or create anonymization salt"""
        salt_file = self.cache_dir / "anonymization_salt"
        
        if salt_file.exists():
            try:
                with open(salt_file, 'r') as f:
                    return f.read().strip()
            except:
                pass
        
        # Generate new salt
        salt = hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]
        
        try:
            with open(salt_file, 'w') as f:
                f.write(salt)
        except:
            pass
        
        return salt
    
    def _anonymize_content(self, content: Dict[str, Any]) -> str:
        """Anonymize content while preserving structure"""
        
        # Convert to string for processing
        content_str = json.dumps(content, sort_keys=True)
        
        # Remove potential personal information
        import re
        
        # Remove email addresses
        content_str = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', content_str)
        
        # Remove URLs
        content_str = re.sub(r'https?://[^\s]+', '[URL]', content_str)
        
        # Remove file paths
        content_str = re.sub(r'/[^\s]*', '[PATH]', content_str)
        
        # Replace long strings with placeholders
        content_str = re.sub(r'"[^"]{50,}"', '"[LONG_STRING]"', content_str)
        
        # Hash with salt for consistent anonymization
        content_hash = hashlib.sha256((content_str + self.anonymization_salt).encode()).hexdigest()[:32]
        
        # Return structured anonymization
        return f"anonymized_{len(content_str)}_{content_hash}"
    
    def _double_anonymize(self, content: str) -> str:
        """Apply additional anonymization for community sharing"""
        return hashlib.sha256((content + "community_salt").encode()).hexdigest()[:24]
    
    def _load_patterns(self):
        """Load patterns from storage"""
        
        # Load local patterns
        try:
            if self.local_patterns_file.exists():
                with open(self.local_patterns_file, 'r') as f:
                    data = json.load(f)
                    self.local_patterns = {
                        k: InteractionPattern.from_dict(v) for k, v in data.items()
                    }
        except Exception as e:
            print(f"⚠️ Could not load local patterns: {e}")
        
        # Load community patterns
        try:
            if self.community_patterns_file.exists():
                with open(self.community_patterns_file, 'r') as f:
                    data = json.load(f)
                    self.community_patterns = {
                        k: InteractionPattern.from_dict(v) for k, v in data.items()
                    }
        except Exception as e:
            print(f"⚠️ Could not load community patterns: {e}")
    
    def _save_patterns(self):
        """Save patterns to storage"""
        
        try:
            # Save local patterns
            with open(self.local_patterns_file, 'w') as f:
                data = {k: v.to_dict() for k, v in self.local_patterns.items()}
                json.dump(data, f, indent=2)
            
            # Save community patterns
            with open(self.community_patterns_file, 'w') as f:
                data = {k: v.to_dict() for k, v in self.community_patterns.items()}
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"⚠️ Could not save patterns: {e}")
    
    def _analyze_local_patterns(self):
        """Analyze local patterns for insights"""
        
        if len(self.local_patterns) < 5:
            return
        
        try:
            # Group patterns by signature type
            by_signature = {}
            for pattern in self.local_patterns.values():
                sig_type = pattern.signature_type
                if sig_type not in by_signature:
                    by_signature[sig_type] = []
                by_signature[sig_type].append(pattern)
            
            # Analyze each signature type
            for sig_type, patterns in by_signature.items():
                if len(patterns) >= 3:
                    analysis_data = self._prepare_pattern_data(patterns)
                    
                    analysis = self.pattern_analyzer(
                        successful_interactions=analysis_data['usage_patterns'],
                        context_type=sig_type,
                        usage_frequency=str(len(patterns))
                    )
                    
                    # Cache the analysis
                    self.optimization_cache[sig_type] = {
                        'patterns': analysis.reusable_patterns,
                        'opportunities': analysis.optimization_opportunities,
                        'generalization': analysis.generalization_potential,
                        'analyzed_at': datetime.now().isoformat()
                    }
        
        except Exception as e:
            print(f"⚠️ Pattern analysis failed: {e}")
    
    def _prepare_pattern_data(self, patterns: List[InteractionPattern]) -> Dict[str, str]:
        """Prepare pattern data for analysis"""
        
        usage_patterns = []
        performance_data = []
        context_variations = set()
        
        for pattern in patterns:
            usage_patterns.append({
                'input': pattern.input_pattern,
                'output': pattern.output_pattern,
                'usage_count': pattern.usage_count
            })
            
            performance_data.append(pattern.success_metrics)
            context_variations.add(pattern.context_type)
        
        return {
            'usage_patterns': json.dumps(usage_patterns),
            'performance_data': json.dumps(performance_data),
            'context_variations': json.dumps(list(context_variations))
        }
    
    def _aggregate_patterns(self, patterns: List[InteractionPattern]) -> Dict[str, Any]:
        """Aggregate patterns for community analysis"""
        
        by_signature = {}
        by_context = {}
        
        for pattern in patterns:
            # Group by signature type
            sig_type = pattern.signature_type
            if sig_type not in by_signature:
                by_signature[sig_type] = {'count': 0, 'total_usage': 0}
            by_signature[sig_type]['count'] += 1
            by_signature[sig_type]['total_usage'] += pattern.usage_count
            
            # Group by context type
            ctx_type = pattern.context_type
            if ctx_type not in by_context:
                by_context[ctx_type] = {'count': 0, 'total_usage': 0}
            by_context[ctx_type]['count'] += 1
            by_context[ctx_type]['total_usage'] += pattern.usage_count
        
        return {
            'by_signature': by_signature,
            'by_context': by_context,
            'total_patterns': len(patterns)
        }
    
    def _calculate_success_metrics(self, patterns: List[InteractionPattern]) -> Dict[str, float]:
        """Calculate aggregate success metrics"""
        
        all_metrics = {}
        
        for pattern in patterns:
            for metric, value in pattern.success_metrics.items():
                if metric not in all_metrics:
                    all_metrics[metric] = []
                all_metrics[metric].append(value)
        
        # Calculate averages
        avg_metrics = {}
        for metric, values in all_metrics.items():
            avg_metrics[metric] = sum(values) / len(values)
        
        return avg_metrics
    
    def _identify_challenges(self, patterns: List[InteractionPattern]) -> List[str]:
        """Identify common challenges from patterns"""
        
        challenges = []
        
        # Analyze success metrics for patterns
        low_quality_count = sum(
            1 for p in patterns 
            if p.success_metrics.get('quality_score', 1.0) < 0.7
        )
        
        if low_quality_count > len(patterns) * 0.2:
            challenges.append("Quality consistency across different contexts")
        
        # Analyze usage patterns
        single_use_count = sum(1 for p in patterns if p.usage_count == 1)
        
        if single_use_count > len(patterns) * 0.5:
            challenges.append("Pattern reusability and generalization")
        
        # Add generic challenges
        challenges.extend([
            "Balancing cost efficiency with quality",
            "Model selection for different complexity levels",
            "Optimizing cache hit rates"
        ])
        
        return challenges[:5]  # Top 5 challenges

# Global instance
_community_learning = None

def get_community_learning() -> CommunityPatternLearning:
    """Get global community learning instance"""
    global _community_learning
    if _community_learning is None:
        _community_learning = CommunityPatternLearning()
    return _community_learning

# Convenience functions
def record_pattern(signature_type: str, context_type: str, inputs: Dict, outputs: Dict, metrics: Dict):
    """Record a successful interaction pattern"""
    learner = get_community_learning()
    learner.record_successful_interaction(signature_type, context_type, inputs, outputs, metrics)

def get_optimization_tips(signature_type: str) -> Dict[str, Any]:
    """Get optimization tips for a signature"""
    learner = get_community_learning()
    return learner.get_optimization_suggestions(signature_type)

def get_community_insights() -> Dict[str, Any]:
    """Get insights from community patterns"""
    learner = get_community_learning()
    return learner.analyze_community_insights()

def share_patterns() -> Dict[str, Any]:
    """Share patterns with community"""
    learner = get_community_learning()
    return learner.share_patterns_anonymously()

def import_patterns(data: Optional[str] = None) -> Dict[str, Any]:
    """Import community patterns"""
    learner = get_community_learning()
    return learner.import_community_patterns(data)

def get_pattern_stats() -> Dict[str, Any]:
    """Get pattern learning statistics"""
    learner = get_community_learning()
    return learner.get_pattern_statistics()