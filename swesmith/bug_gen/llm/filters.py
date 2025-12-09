"""
Entity filters for selecting specific types of code entities during bug generation.

Filters allow customization of which entities (functions, classes, files) are considered
as candidates for bug injection. This enables specialized bug generation for different
types of targets (e.g., build files, configuration files, specific code patterns).
"""

from swesmith.constants import CodeEntity


class EntityFilter:
    """Base class for filtering code entities."""

    def __call__(self, entity: CodeEntity) -> bool:
        """
        Return True if entity should be included, False otherwise.

        This method is called for each extracted entity to determine if it should
        be included in the candidates list for bug generation.
        """
        raise NotImplementedError


class GradleFilter(EntityFilter):
    """Filter for Gradle build configuration files."""

    def __call__(self, entity: CodeEntity) -> bool:
        """Include only main Gradle build files, excluding build tool directories."""
        file_path_lower = entity.file_path.lower()

        if not any(
                filename in file_path_lower
                for filename in [
                    "build.gradle",
                    "settings.gradle",
                    "build.gradle.kts",
                    "settings.gradle.kts",
                ]
        ):
            return False

        if "buildsrc" in file_path_lower or "/.gradle/" in entity.file_path:
            return False

        return True


# Registry of available filters
# To add a custom filter:
# 1. Create a class that inherits from EntityFilter
# 2. Implement __call__(entity) to return True/False for inclusion
# 3. Add it to the ENTITY_FILTERS registry below
ENTITY_FILTERS: dict[str, type[EntityFilter]] = {
    "gradle": GradleFilter,
}
