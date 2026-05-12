from dataclasses import dataclass
from importlib.metadata import Distribution
from importlib.metadata import version as metadata_version

from packaging.metadata import Metadata
from packaging.version import Version
from packaging.version import parse as parse_version

from vcf_generator_lite.constants import APP_COPYRIGHT, EMAIL_AUTHOR, URL_RELEASES, URL_REPOSITORY

__all__ = ["app_metadata", "app_version_variants"]


def get_windows_file_info_version(version: Version) -> tuple[int, int, int, int]:
    build = 0
    match version.pre:
        case ("a", _):
            build += 10000
        case ("b", _):
            build += 20000
        case ("rc", _):
            build += 30000
        case _:
            if not version.is_devrelease:
                build += 40000
    if version.pre:
        build += version.pre[1] * 100
    if version.post is not None:
        build += version.post * 10
    if version.dev is not None:
        build += version.dev
    return (
        version.major,
        version.minor,
        version.micro,
        build,
    )


def get_semantic_version(version: Version) -> str:
    sem_ver = f"{version.major}.{version.minor}.{version.micro}"
    if version.pre:
        match version.pre[0]:
            case "a":
                sem_ver += "-alpha"
            case "b":
                sem_ver += "-beta"
            case "rc":
                sem_ver += "-rc"

    if version.pre and version.pre[1]:
        sem_ver += f".{version.pre[1]}"

    return sem_ver


@dataclass(kw_only=True)
class VersionVariants:
    wheel: str
    semantic: str
    windows: str
    windows_ffi: tuple[int, int, int, int]

    @staticmethod
    def from_version_wheel(version_wheel: str) -> "VersionVariants":
        parsed: Version = parse_version(version_wheel)
        version_windows_ffi = get_windows_file_info_version(parsed)
        return VersionVariants(
            wheel=version_wheel,
            semantic=get_semantic_version(parsed),
            windows=".".join(map(str, version_windows_ffi)),
            windows_ffi=version_windows_ffi,
        )


@dataclass(kw_only=True)
class AppMetadata:
    display_name: str
    repository: str | None
    bug_tracker: str | None
    author: str | None
    author_email: str | None
    summary: str | None
    description: str | None
    copyright: str | None
    release_notes: str | None


def get_pkg_metadata(name: str) -> Metadata:
    _metadata_raw = Distribution.from_name(name).read_text("METADATA")
    if _metadata_raw is None:
        raise RuntimeError("Failed to read metadata")
    return Metadata.from_email(_metadata_raw)


app_pkg_metadata = get_pkg_metadata("vcf_generator_lite")
app_metadata = AppMetadata(
    display_name="VCF Generator Lite",
    repository=URL_REPOSITORY,
    bug_tracker=app_pkg_metadata.project_urls["Issues"] if app_pkg_metadata.project_urls else None,
    author=app_pkg_metadata.author,
    author_email=EMAIL_AUTHOR,
    summary=app_pkg_metadata.summary,
    description=app_pkg_metadata.description,
    copyright=APP_COPYRIGHT,
    release_notes=URL_RELEASES,
)
app_version_variants = VersionVariants.from_version_wheel(metadata_version("vcf_generator_lite"))
