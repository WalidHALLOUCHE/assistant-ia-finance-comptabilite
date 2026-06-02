"""Security utilities for sensitive operations."""

import os
from typing import Optional


class SecurityManager:
    """Manages security-related operations."""

    @staticmethod
    def check_api_keys_in_code() -> bool:
        """Verify that no API keys are hardcoded in the codebase."""
        import glob

        patterns = ["sk-", "AIza", "gsk_", "GEMINI_", "GROQ_"]
        python_files = glob.glob("src/**/*.py", recursive=True)

        for filepath in python_files:
            with open(filepath) as f:
                content = f.read()
                for pattern in patterns:
                    if pattern in content and "getenv" not in content:
                        return False
        return True

    @staticmethod
    def mask_sensitive_info(value: Optional[str], visible_chars: int = 4) -> str:
        """Mask sensitive information like API keys."""
        if not value:
            return "[NOT CONFIGURED]"
        if len(value) <= visible_chars:
            return "***"
        return value[:visible_chars] + "*" * (len(value) - visible_chars)

    @staticmethod
    def validate_env_file_exists() -> bool:
        """Check if .env file exists."""
        return os.path.exists(".env")

    @staticmethod
    def validate_no_secrets_in_git() -> list[str]:
        """Check common files for hardcoded secrets."""
        warnings = []

        if not os.path.exists(".gitignore"):
            warnings.append("⚠️  .gitignore not found")
        else:
            with open(".gitignore") as f:
                if ".env" not in f.read():
                    warnings.append("⚠️  .env not properly ignored in .gitignore")

        if os.path.exists(".env"):
            warnings.append("⚠️  .env file should not be committed to git")

        return warnings
