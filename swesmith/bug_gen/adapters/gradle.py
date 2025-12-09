"""
Adapter for extracting Gradle build files as candidates for bug generation.

Unlike other adapters that extract functions/classes, this adapter treats
entire Gradle build files as single entities for build configuration bug injection.
"""

import os
from swesmith.constants import CodeEntity


class GradleEntity(CodeEntity):
    @property
    def name(self) -> str:
        """Return the name of the build file (e.g., build.gradle, settings.gradle)."""
        return os.path.basename(self.file_path)

    @property
    def signature(self) -> str:
        """For Gradle files, signature is the file name."""
        return self.name

    @property
    def stub(self) -> str:
        """Return empty stub - not applicable for Gradle files."""
        return ""


def get_entities_from_file_gradle(
    entities: list[GradleEntity],
    file_path: str,
    max_entities: int = -1,
) -> None:
    """
    Parse a .gradle or .gradle.kts file and treat the entire file as a single entity.

    Args:
        entities: List to append the GradleEntity to
        file_path: Path to the gradle file
        max_entities: Maximum number of entities (-1 for unlimited)
    """
    # Stop if we've hit the limit
    if 0 <= max_entities == len(entities):
        return

    # Read the entire file content
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()
    except Exception:
        return

    # Skip empty files
    if not file_content.strip():
        return

    # Count lines for line_end
    lines = file_content.splitlines()

    # Create a single entity representing the entire build file
    entities.append(
        GradleEntity(
            file_path=file_path,
            indent_level=0,
            indent_size=4,  # Default, not particularly relevant for full-file entities
            line_start=1,
            line_end=len(lines),
            node=None,  # No tree-sitter node for gradle files
            src_code=file_content,
        )
    )
