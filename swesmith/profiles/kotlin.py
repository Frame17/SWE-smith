import re

from dataclasses import dataclass, field
from swebench.harness.constants import TestStatus
from swesmith.profiles.base import RepoProfile, registry


@dataclass
class KotlinProfile(RepoProfile):
    """
    Profile for Kotlin repositories.
    """


@dataclass
class Moshibb061b05(KotlinProfile):
    org_gh = "BlackCatsOfMidnight"
    owner: str = "square"
    repo: str = "moshi"
    commit: str = "bb061b05cb07cfd6344ef368d3684161f830598f"
    test_cmd: str = "./gradlew test --no-daemon --console=plain"
    eval_sets: set[str] = field(
        default_factory=lambda: {"SWE-bench/SWE-bench_Multilingual"}
    )

    @property
    def image_name(self) -> str:
        return "moshi"

    @property
    def dockerfile(self):
        return f"""FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
RUN apt-get update && apt-get install -y git openjdk-17-jdk
RUN git clone https://github.com/{self.mirror_name} /testbed
WORKDIR /testbed
RUN ./gradlew build -x test --no-daemon
"""

    def log_parser(self, log: str) -> dict[str, str]:
        test_status_map = {}
        # Pattern for Gradle test output
        # Example: "com.squareup.moshi.AdapterMethodsTest > testMethod PASSED"
        # Example: "com.squareup.moshi.AdapterMethodsTest > testMethod FAILED"
        pattern = r"^([\w.]+)\s+>\s+([\w]+)\s+(PASSED|FAILED|SKIPPED)"
        for line in log.split("\n"):
            match = re.match(pattern, line.strip())
            if match:
                test_class = match.group(1)
                test_method = match.group(2)
                status = match.group(3)
                test_name = f"{test_class}.{test_method}"
                if status == "PASSED":
                    test_status_map[test_name] = TestStatus.PASSED.value
                elif status == "FAILED":
                    test_status_map[test_name] = TestStatus.FAILED.value
        return test_status_map


# Register all Kotlin profiles with the global registry
for name, obj in list(globals().items()):
    if (
        isinstance(obj, type)
        and issubclass(obj, KotlinProfile)
        and obj.__name__ != "KotlinProfile"
    ):
        registry.register_profile(obj)
