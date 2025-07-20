"""Tests for AtlasCoderEngine core functionality."""

import pytest
import os
from unittest.mock import patch, MagicMock
from atlas_coder.core.engine import AtlasCoderEngine, CostTracker, ModelConfig


class TestCostTracker:
    """Test the CostTracker functionality."""
    
    def test_cost_tracker_initialization(self):
        """Test CostTracker initialization with default values."""
        tracker = CostTracker()
        assert tracker.daily_budget == 1.0
        assert tracker.current_cost == 0.0
        assert tracker.calls_made == 0
    
    def test_cost_tracker_can_make_call(self):
        """Test budget checking functionality."""
        tracker = CostTracker(daily_budget=1.0)
        
        # Should be able to make calls within budget
        assert tracker.can_make_call(0.50) is True
        
        # Should not be able to make calls that exceed budget
        assert tracker.can_make_call(1.50) is False
    
    def test_cost_tracker_add_cost(self):
        """Test cost tracking functionality."""
        tracker = CostTracker()
        
        tracker.add_cost(0.25)
        assert tracker.current_cost == 0.25
        assert tracker.calls_made == 1
        
        tracker.add_cost(0.30)
        assert tracker.current_cost == 0.55
        assert tracker.calls_made == 2


class TestModelConfig:
    """Test ModelConfig functionality."""
    
    def test_model_config_creation(self):
        """Test ModelConfig creation with required fields."""
        config = ModelConfig(
            name="test/model",
            cost_per_million_tokens=0.10,
            max_tokens=1000000
        )
        
        assert config.name == "test/model"
        assert config.cost_per_million_tokens == 0.10
        assert config.max_tokens == 1000000
        assert config.supports_json is True  # default
        assert config.provider == "openrouter"  # default


class TestAtlasCoderEngine:
    """Test AtlasCoderEngine functionality."""
    
    def test_engine_initialization_local_only(self):
        """Test engine initialization with local-only strategy."""
        with patch.dict(os.environ, {}, clear=True):
            engine = AtlasCoderEngine(model_strategy="local-only")
            assert engine.model_strategy == "local-only"
            assert engine.cost_tracker.daily_budget == 1.0
    
    def test_engine_initialization_cost_optimal(self):
        """Test engine initialization with cost-optimal strategy."""
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}):
            with patch('dspy.LM') as mock_lm:
                with patch('dspy.configure') as mock_configure:
                    engine = AtlasCoderEngine(model_strategy="cost-optimal")
                    assert engine.model_strategy == "cost-optimal"
                    mock_lm.assert_called_once()
                    mock_configure.assert_called_once()
    
    def test_estimate_cost_local_only(self):
        """Test cost estimation for local-only strategy."""
        with patch.dict(os.environ, {}, clear=True):
            engine = AtlasCoderEngine(model_strategy="local-only")
            cost = engine.estimate_cost(1000, 500)
            assert cost == 0.0  # Local models have no cost
    
    def test_estimate_cost_cloud_model(self):
        """Test cost estimation for cloud models."""
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}):
            with patch('dspy.LM'):
                with patch('dspy.configure'):
                    engine = AtlasCoderEngine(model_strategy="cost-optimal")
                    cost = engine.estimate_cost(1000, 500)
                    expected_cost = (1500 / 1_000_000) * 0.075  # Using cost-optimal rate
                    assert cost == expected_cost
    
    def test_can_execute_within_budget(self):
        """Test execution budget checking."""
        with patch.dict(os.environ, {}, clear=True):
            engine = AtlasCoderEngine(model_strategy="local-only", daily_budget=1.0)
            # Local strategy should always allow execution (no cost)
            assert engine.can_execute() is True
    
    def test_get_status(self):
        """Test status reporting functionality."""
        with patch.dict(os.environ, {}, clear=True):
            engine = AtlasCoderEngine(model_strategy="local-only")
            status = engine.get_status()
            
            assert status["model_strategy"] == "local-only"
            assert status["daily_budget"] == 1.0
            assert status["current_cost"] == 0.0
            assert status["remaining_budget"] == 1.0
            assert status["calls_made"] == 0
            assert status["can_make_calls"] is True
    
    def test_record_usage(self):
        """Test usage recording functionality."""
        with patch.dict(os.environ, {}, clear=True):
            engine = AtlasCoderEngine(model_strategy="local-only")
            
            initial_calls = engine.cost_tracker.calls_made
            engine.record_usage(1000, 500)
            
            assert engine.cost_tracker.calls_made == initial_calls + 1
    
    @patch('dspy.LM')
    @patch('dspy.configure')
    def test_missing_api_key_raises_error(self, mock_configure, mock_lm):
        """Test that missing API key raises appropriate error."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="OPENROUTER_API_KEY environment variable required"):
                AtlasCoderEngine(model_strategy="cost-optimal")


class TestIntegration:
    """Integration tests for the engine."""
    
    def test_engine_workflow_local_only(self):
        """Test complete engine workflow with local-only strategy."""
        with patch.dict(os.environ, {}, clear=True):
            engine = AtlasCoderEngine(model_strategy="local-only")
            
            # Check that we can execute
            assert engine.can_execute() is True
            
            # Mock a DSPy module execution
            mock_module = MagicMock()
            mock_module.return_value = "test result"
            
            # Execute with tracking should work
            result = engine.execute_with_tracking(mock_module, test_param="value")
            assert result == "test result"
            
            # Usage should be recorded
            assert engine.cost_tracker.calls_made == 1
            
            # Status should reflect the change
            status = engine.get_status()
            assert status["calls_made"] == 1


if __name__ == "__main__":
    pytest.main([__file__])