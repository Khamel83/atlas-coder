"""
Advanced Caching System for Atlas Coder DSPy
Smart caching to make free models incredibly effective
"""

import os
import json
import hashlib
import time
import pickle
from typing import Any, Dict, Optional, List
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class CacheEntry:
    """Single cache entry with metadata"""
    key: str
    signature: str
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    model: str
    timestamp: float
    success: bool
    execution_time: float
    hit_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CacheEntry':
        """Create from dictionary"""
        return cls(**data)

class SignatureCache:
    """Smart caching for DSPy signatures and modules"""
    
    def __init__(self, cache_dir: str = "./dspy_cache", max_entries: int = 10000):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.max_entries = max_entries
        
        # Cache storage
        self.memory_cache: Dict[str, CacheEntry] = {}
        self.cache_file = self.cache_dir / "signature_cache.json"
        self.stats_file = self.cache_dir / "cache_stats.json"
        
        # Performance tracking
        self.stats = {
            "total_requests": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "total_execution_time": 0.0,
            "cache_size": 0
        }
        
        self._load_cache()
        self._load_stats()
    
    def _generate_cache_key(self, signature: str, inputs: Dict[str, Any], model: str) -> str:
        """Generate deterministic cache key"""
        # Normalize inputs for consistent hashing
        normalized_inputs = self._normalize_inputs(inputs)
        
        # Create hash from signature + inputs + model
        cache_data = {
            "signature": signature,
            "inputs": normalized_inputs,
            "model": model
        }
        
        cache_string = json.dumps(cache_data, sort_keys=True)
        return hashlib.sha256(cache_string.encode()).hexdigest()
    
    def _normalize_inputs(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize inputs for consistent caching"""
        normalized = {}
        
        for key, value in inputs.items():
            if isinstance(value, str):
                # Normalize whitespace and remove leading/trailing spaces
                normalized[key] = " ".join(value.strip().split())
            else:
                normalized[key] = value
        
        return normalized
    
    def _load_cache(self):
        """Load cache from disk"""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r') as f:
                    data = json.load(f)
                    
                for key, entry_data in data.items():
                    self.memory_cache[key] = CacheEntry.from_dict(entry_data)
                    
                print(f"💾 Loaded {len(self.memory_cache)} cache entries")
        except Exception as e:
            print(f"⚠️ Cache load failed: {e}")
            self.memory_cache = {}
    
    def _save_cache(self):
        """Save cache to disk"""
        try:
            # Convert cache to serializable format
            cache_data = {
                key: entry.to_dict() 
                for key, entry in self.memory_cache.items()
            }
            
            with open(self.cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
                
        except Exception as e:
            print(f"⚠️ Cache save failed: {e}")
    
    def _load_stats(self):
        """Load performance statistics"""
        try:
            if self.stats_file.exists():
                with open(self.stats_file, 'r') as f:
                    self.stats.update(json.load(f))
        except Exception as e:
            print(f"⚠️ Stats load failed: {e}")
    
    def _save_stats(self):
        """Save performance statistics"""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except Exception as e:
            print(f"⚠️ Stats save failed: {e}")
    
    def get(self, signature: str, inputs: Dict[str, Any], model: str) -> Optional[Dict[str, Any]]:
        """Get cached result if available"""
        cache_key = self._generate_cache_key(signature, inputs, model)
        
        self.stats["total_requests"] += 1
        
        if cache_key in self.memory_cache:
            entry = self.memory_cache[cache_key]
            entry.hit_count += 1
            
            self.stats["cache_hits"] += 1
            
            print(f"🎯 Cache hit for {signature[:30]}... (used {entry.hit_count} times)")
            return entry.outputs
        
        self.stats["cache_misses"] += 1
        return None
    
    def put(self, signature: str, inputs: Dict[str, Any], outputs: Dict[str, Any], 
            model: str, execution_time: float, success: bool = True):
        """Store result in cache"""
        cache_key = self._generate_cache_key(signature, inputs, model)
        
        entry = CacheEntry(
            key=cache_key,
            signature=signature,
            inputs=self._normalize_inputs(inputs),
            outputs=outputs,
            model=model,
            timestamp=time.time(),
            success=success,
            execution_time=execution_time
        )
        
        self.memory_cache[cache_key] = entry
        self.stats["total_execution_time"] += execution_time
        self.stats["cache_size"] = len(self.memory_cache)
        
        # Cleanup if cache gets too large
        if len(self.memory_cache) > self.max_entries:
            self._cleanup_cache()
        
        print(f"💾 Cached result for {signature[:30]}...")
    
    def _cleanup_cache(self):
        """Remove old or least-used cache entries"""
        if len(self.memory_cache) <= self.max_entries * 0.8:
            return
        
        # Sort by last access time and hit count
        entries = list(self.memory_cache.items())
        entries.sort(key=lambda x: (x[1].hit_count, x[1].timestamp))
        
        # Keep the most useful entries
        keep_count = int(self.max_entries * 0.8)
        entries_to_keep = entries[-keep_count:]
        
        self.memory_cache = {key: entry for key, entry in entries_to_keep}
        
        print(f"🧹 Cache cleanup: kept {len(self.memory_cache)} most useful entries")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics"""
        hit_rate = 0.0
        if self.stats["total_requests"] > 0:
            hit_rate = self.stats["cache_hits"] / self.stats["total_requests"]
        
        avg_execution_time = 0.0
        if self.stats["cache_misses"] > 0:
            avg_execution_time = self.stats["total_execution_time"] / self.stats["cache_misses"]
        
        return {
            **self.stats,
            "hit_rate": hit_rate,
            "avg_execution_time": avg_execution_time,
            "cache_efficiency": hit_rate * 100,
            "memory_usage_mb": self._get_cache_size_mb()
        }
    
    def _get_cache_size_mb(self) -> float:
        """Estimate cache memory usage in MB"""
        try:
            cache_size = len(pickle.dumps(self.memory_cache))
            return cache_size / (1024 * 1024)
        except:
            return 0.0
    
    def save_all(self):
        """Save cache and stats to disk"""
        self._save_cache()
        self._save_stats()
    
    def clear(self):
        """Clear all cache entries"""
        self.memory_cache.clear()
        self.stats = {
            "total_requests": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "total_execution_time": 0.0,
            "cache_size": 0
        }
        print("🗑️ Cache cleared")

class OptimizationCache:
    """Cache for DSPy optimization results and patterns"""
    
    def __init__(self, cache_dir: str = "./dspy_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        self.optimization_file = self.cache_dir / "optimizations.json"
        self.patterns_file = self.cache_dir / "successful_patterns.json"
        
        self.optimizations = {}
        self.patterns = {}
        
        self._load_optimizations()
        self._load_patterns()
    
    def _load_optimizations(self):
        """Load optimization results"""
        try:
            if self.optimization_file.exists():
                with open(self.optimization_file, 'r') as f:
                    self.optimizations = json.load(f)
        except Exception as e:
            print(f"⚠️ Optimization load failed: {e}")
    
    def _load_patterns(self):
        """Load successful patterns"""
        try:
            if self.patterns_file.exists():
                with open(self.patterns_file, 'r') as f:
                    self.patterns = json.load(f)
        except Exception as e:
            print(f"⚠️ Patterns load failed: {e}")
    
    def save_optimization(self, signature: str, optimization_data: Dict[str, Any]):
        """Save optimization result"""
        self.optimizations[signature] = {
            "data": optimization_data,
            "timestamp": time.time()
        }
        
        self._save_optimizations()
    
    def get_optimization(self, signature: str) -> Optional[Dict[str, Any]]:
        """Get cached optimization for signature"""
        return self.optimizations.get(signature, {}).get("data")
    
    def save_successful_pattern(self, pattern_type: str, pattern_data: Dict[str, Any]):
        """Save successful execution pattern"""
        if pattern_type not in self.patterns:
            self.patterns[pattern_type] = []
        
        pattern_entry = {
            "data": pattern_data,
            "timestamp": time.time(),
            "success_count": 1
        }
        
        self.patterns[pattern_type].append(pattern_entry)
        self._save_patterns()
    
    def get_successful_patterns(self, pattern_type: str) -> List[Dict[str, Any]]:
        """Get successful patterns for a type"""
        return self.patterns.get(pattern_type, [])
    
    def _save_optimizations(self):
        """Save optimizations to disk"""
        try:
            with open(self.optimization_file, 'w') as f:
                json.dump(self.optimizations, f, indent=2)
        except Exception as e:
            print(f"⚠️ Optimization save failed: {e}")
    
    def _save_patterns(self):
        """Save patterns to disk"""
        try:
            with open(self.patterns_file, 'w') as f:
                json.dump(self.patterns, f, indent=2)
        except Exception as e:
            print(f"⚠️ Patterns save failed: {e}")

# Global cache instances
_signature_cache = None
_optimization_cache = None

def get_signature_cache() -> SignatureCache:
    """Get or create global signature cache"""
    global _signature_cache
    if _signature_cache is None:
        _signature_cache = SignatureCache()
    return _signature_cache

def get_optimization_cache() -> OptimizationCache:
    """Get or create global optimization cache"""
    global _optimization_cache
    if _optimization_cache is None:
        _optimization_cache = OptimizationCache()
    return _optimization_cache