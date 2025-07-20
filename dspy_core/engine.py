"""
Atlas Coder DSPy Engine
Core engine for systematic programming with free models
"""

import os
import dspy
from typing import Optional, Dict, Any
import json
import time
from .cache import get_signature_cache

class AtlasCoderEngine:
    """
    Revolutionary DSPy-powered coding engine
    Replaces prompt engineering with systematic programming
    """
    
    def __init__(self, model: Optional[str] = None, cache_dir: str = "./dspy_cache"):
        """
        Initialize the DSPy engine with free model support
        
        Args:
            model: Model to use (defaults to free options)
            cache_dir: Directory for caching optimizations
        """
        self.model = model or self._get_default_model()
        self.cache_dir = cache_dir
        self._setup_model()
        self._setup_cache()
        
        # Initialize smart caching
        self.signature_cache = get_signature_cache()
        
    def _get_default_model(self) -> str:
        """Get the best available free model"""
        # Priority order for free models
        free_models = [
            "ollama/llama3.2",           # Local Ollama if available
            "ollama/codellama",          # Code-focused local model
            "openrouter/google/gemini-1.5-flash",  # Free API tier
            "openrouter/meta-llama/llama-3.2-3b-instruct:free",  # Free tier
        ]
        
        # Use environment variable if set
        env_model = os.getenv("OPENAI_MODEL")
        if env_model:
            return env_model
            
        # Default to first free option
        return free_models[0]
    
    def _setup_model(self):
        """Configure DSPy with the selected model"""
        try:
            # Configure based on model type
            if self.model.startswith("ollama/"):
                # Local Ollama model
                model_name = self.model.replace("ollama/", "")
                self.lm = dspy.LM(
                    model=f"ollama/{model_name}",
                    api_base="http://localhost:11434",
                    api_key="",  # Ollama doesn't need API key
                    max_tokens=4000
                )
            elif self.model.startswith("openrouter/"):
                # OpenRouter free tier
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    raise ValueError("OPENAI_API_KEY required for OpenRouter models")
                    
                self.lm = dspy.LM(
                    model=self.model,
                    api_base="https://openrouter.ai/api/v1",
                    api_key=api_key,
                    max_tokens=4000
                )
            else:
                # Generic OpenAI-compatible API
                api_key = os.getenv("OPENAI_API_KEY", "")
                api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
                
                self.lm = dspy.LM(
                    model=self.model,
                    api_base=api_base,
                    api_key=api_key,
                    max_tokens=4000
                )
            
            # Configure DSPy to use this model
            dspy.configure(lm=self.lm)
            print(f"✅ DSPy configured with model: {self.model}")
            
        except Exception as e:
            print(f"⚠️ Model setup failed: {e}")
            print("📝 Falling back to OpenRouter free tier")
            self._setup_fallback_model()
    
    def _setup_fallback_model(self):
        """Setup fallback to OpenRouter free tier"""
        try:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("No API key available for fallback")
                
            self.lm = dspy.LM(
                model="openrouter/google/gemini-1.5-flash",
                api_base="https://openrouter.ai/api/v1",
                api_key=api_key,
                max_tokens=4000
            )
            dspy.configure(lm=self.lm)
            self.model = "openrouter/google/gemini-1.5-flash"
            print(f"✅ Fallback model configured: {self.model}")
            
        except Exception as e:
            print(f"❌ Fallback setup failed: {e}")
            print("💡 Please set OPENAI_API_KEY or install Ollama for local models")
            raise
    
    def _setup_cache(self):
        """Setup local caching for optimization"""
        os.makedirs(self.cache_dir, exist_ok=True)
        self.cache_file = os.path.join(self.cache_dir, "dspy_cache.json")
        
        # Load existing cache
        try:
            with open(self.cache_file, 'r') as f:
                self.cache = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.cache = {}
            
        print(f"💾 Cache initialized: {len(self.cache)} entries")
    
    def save_cache(self):
        """Save optimization cache to disk"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except Exception as e:
            print(f"⚠️ Cache save failed: {e}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model configuration"""
        cache_stats = self.signature_cache.get_stats()
        
        return {
            "model": self.model,
            "cache_entries": cache_stats["cache_size"],
            "cache_hit_rate": f"{cache_stats['cache_efficiency']:.1f}%",
            "cache_dir": self.cache_dir,
            "is_local": self.model.startswith("ollama/"),
            "is_free": any(x in self.model for x in ["free", "ollama", "gemini"]),
            "total_requests": cache_stats["total_requests"],
            "cache_memory_mb": f"{cache_stats['memory_usage_mb']:.1f}MB"
        }
    
    def test_model(self) -> bool:
        """Test if the model is working correctly"""
        try:
            # Simple test prediction
            test_signature = dspy.Signature("question -> answer")
            test_module = dspy.Predict(test_signature)
            
            result = test_module(question="What is 2+2?")
            
            if result and hasattr(result, 'answer'):
                print(f"✅ Model test successful: {result.answer}")
                return True
            else:
                print("❌ Model test failed: No response")
                return False
                
        except Exception as e:
            print(f"❌ Model test failed: {e}")
            return False

# Global engine instance
_engine = None

def get_engine() -> AtlasCoderEngine:
    """Get or create the global DSPy engine instance"""
    global _engine
    if _engine is None:
        _engine = AtlasCoderEngine()
    return _engine

def initialize_engine(model: Optional[str] = None) -> AtlasCoderEngine:
    """Initialize the DSPy engine with specific model"""
    global _engine
    _engine = AtlasCoderEngine(model=model)
    return _engine