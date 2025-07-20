"""Tests for CLI functionality."""

import pytest
from click.testing import CliRunner
from unittest.mock import patch, MagicMock
import os

from atlas_coder.cli.main import cli


class TestCLI:
    """Test CLI command functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        self.runner = CliRunner()
    
    def test_version_command(self):
        """Test version command."""
        result = self.runner.invoke(cli, ['version'])
        assert result.exit_code == 0
        assert "Atlas Coder Version: 1.0.0" in result.output
    
    def test_help_command(self):
        """Test help command."""
        result = self.runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert "Atlas Coder CLI" in result.output
        assert "Commands:" in result.output
    
    def test_status_command_local_only(self):
        """Test status command with local-only strategy."""
        with patch.dict(os.environ, {}, clear=True):
            result = self.runner.invoke(cli, ['--model-strategy', 'local-only', 'status'])
            assert result.exit_code == 0
            assert "Atlas Coder Status" in result.output
            assert "local-only" in result.output
    
    def test_cost_report_command(self):
        """Test cost report command."""
        with patch.dict(os.environ, {}, clear=True):
            result = self.runner.invoke(cli, ['--model-strategy', 'local-only', 'cost-report'])
            assert result.exit_code == 0
            assert "Cost Report" in result.output
            assert "Daily Budget" in result.output
    
    def test_yolo_mode_prompt(self):
        """Test YOLO mode confirmation prompt."""
        # Test cancelling YOLO mode
        result = self.runner.invoke(cli, ['--yolo', 'version'], input='n\n')
        assert result.exit_code == 1
        assert "YOLO mode cancelled" in result.output
    
    def test_missing_api_key_error(self):
        """Test error when API key is missing for cloud models."""
        with patch.dict(os.environ, {}, clear=True):
            result = self.runner.invoke(cli, ['--model-strategy', 'cost-optimal', 'status'])
            assert result.exit_code == 1
            assert "OPENROUTER_API_KEY environment variable required" in result.output
    
    @patch('atlas_coder.core.workflows.WorkflowOrchestrator')
    def test_generate_command(self, mock_orchestrator):
        """Test generate command."""
        mock_instance = MagicMock()
        mock_instance.generate.return_value = "✅ Code generated successfully"
        mock_orchestrator.return_value = mock_instance
        
        with patch.dict(os.environ, {}, clear=True):
            result = self.runner.invoke(cli, [
                '--model-strategy', 'local-only',
                'generate', 'test requirements'
            ])
            
            assert result.exit_code == 0
            mock_instance.generate.assert_called_once()
    
    @patch('atlas_coder.core.workflows.WorkflowOrchestrator')
    def test_analyze_command(self, mock_orchestrator):
        """Test analyze command."""
        mock_instance = MagicMock()
        mock_instance.analyze.return_value = "✅ Analysis completed"
        mock_orchestrator.return_value = mock_instance
        
        with patch.dict(os.environ, {}, clear=True):
            # Create a temporary file for testing
            with self.runner.isolated_filesystem():
                with open('test_file.py', 'w') as f:
                    f.write('print("hello")')
                
                result = self.runner.invoke(cli, [
                    '--model-strategy', 'local-only',
                    'analyze', 'test_file.py'
                ])
                
                assert result.exit_code == 0
                mock_instance.analyze.assert_called_once()
    
    @patch('atlas_coder.core.workflows.WorkflowOrchestrator')
    def test_fix_bug_command(self, mock_orchestrator):
        """Test fix-bug command."""
        mock_instance = MagicMock()
        mock_instance.fix_bug.return_value = "✅ Bug fixed"
        mock_orchestrator.return_value = mock_instance
        
        with patch.dict(os.environ, {}, clear=True):
            # Create a temporary file for testing
            with self.runner.isolated_filesystem():
                with open('buggy_file.py', 'w') as f:
                    f.write('def broken(): return 1/0')
                
                result = self.runner.invoke(cli, [
                    '--model-strategy', 'local-only',
                    'fix-bug', 'buggy_file.py',
                    '--error', 'ZeroDivisionError'
                ])
                
                assert result.exit_code == 0
                mock_instance.fix_bug.assert_called_once()
    
    def test_git_commands_placeholder(self):
        """Test git command placeholders."""
        result = self.runner.invoke(cli, ['git', '--help'])
        assert result.exit_code == 0
        assert "git" in result.output.lower()
        
        result = self.runner.invoke(cli, ['git', 'setup'])
        assert result.exit_code == 0
        assert "coming soon" in result.output.lower()


class TestCLIValidation:
    """Test CLI input validation."""
    
    def setup_method(self):
        """Set up test environment."""
        self.runner = CliRunner()
    
    def test_invalid_model_strategy(self):
        """Test invalid model strategy parameter."""
        result = self.runner.invoke(cli, ['--model-strategy', 'invalid', 'version'])
        assert result.exit_code != 0
        assert "Invalid value" in result.output
    
    def test_invalid_budget(self):
        """Test invalid budget parameter."""
        result = self.runner.invoke(cli, ['--budget', 'invalid', 'version'])
        assert result.exit_code != 0
    
    def test_nonexistent_file_analyze(self):
        """Test analyze command with nonexistent file."""
        result = self.runner.invoke(cli, [
            '--model-strategy', 'local-only',
            'analyze', 'nonexistent_file.py'
        ])
        assert result.exit_code != 0
    
    def test_nonexistent_file_fix_bug(self):
        """Test fix-bug command with nonexistent file."""
        result = self.runner.invoke(cli, [
            '--model-strategy', 'local-only',
            'fix-bug', 'nonexistent_file.py'
        ])
        assert result.exit_code != 0


if __name__ == "__main__":
    pytest.main([__file__])