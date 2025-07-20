"""Aider integration for Atlas Coder.

This module provides integration with Aider for git patch generation
and application in Atlas Coder workflows.
"""

import subprocess
import tempfile
from pathlib import Path
from typing import Any


class AiderIntegration:
    """Integration with Aider for git-based code changes."""

    def __init__(self, repo_path: str = "."):
        """Initialize Aider integration.

        Args:
            repo_path: Path to git repository
        """
        self.repo_path = Path(repo_path)

    def is_available(self) -> bool:
        """Check if Aider is available in the system."""
        try:
            result = subprocess.run(
                ["aider", "--version"], capture_output=True, text=True
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False

    def generate_patch(
        self, file_path: str, changes: str, commit_message: str
    ) -> str | None:
        """Generate a git patch using Aider.

        Args:
            file_path: Path to file to modify
            changes: Description of changes to make
            commit_message: Commit message for the patch

        Returns:
            Patch content as string, or None if failed
        """
        if not self.is_available():
            return None

        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
                f.write(f"Modify {file_path}:\n{changes}")
                instructions_file = f.name

            # Run aider with instructions
            cmd = [
                "aider",
                "--no-auto-commits",
                "--message",
                commit_message,
                file_path,
                "--file",
                instructions_file,
            ]

            result = subprocess.run(
                cmd, cwd=self.repo_path, capture_output=True, text=True
            )

            if result.returncode == 0:
                # Generate patch from the changes
                patch_result = subprocess.run(
                    ["git", "diff", "--cached"],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True,
                )
                return patch_result.stdout

        except Exception:
            pass

        finally:
            # Clean up
            try:
                Path(instructions_file).unlink()
            except Exception:
                pass

        return None

    def apply_patch(self, patch_content: str) -> bool:
        """Apply a git patch.

        Args:
            patch_content: Patch content to apply

        Returns:
            True if successful, False otherwise
        """
        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".patch", delete=False) as f:
                f.write(patch_content)
                patch_file = f.name

            result = subprocess.run(
                ["git", "apply", patch_file],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )

            Path(patch_file).unlink()
            return result.returncode == 0

        except Exception:
            return False

    def create_backup_patch(self, description: str = "Atlas Coder backup") -> str | None:
        """Create a backup patch of current changes.

        Args:
            description: Description for the backup

        Returns:
            Patch content as string, or None if failed
        """
        try:
            result = subprocess.run(
                ["git", "diff", "HEAD"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )

            if result.returncode == 0 and result.stdout.strip():
                return result.stdout

        except Exception:
            pass

        return None


def get_aider_integration(repo_path: str = ".") -> AiderIntegration:
    """Factory function to get Aider integration instance."""
    return AiderIntegration(repo_path)