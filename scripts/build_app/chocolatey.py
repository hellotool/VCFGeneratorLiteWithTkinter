import hashlib
import shutil
import subprocess
from collections.abc import Mapping
from contextlib import contextmanager
from pathlib import Path
from string import Template

from scripts.app_metadata import app_metadata, app_version_variants
from scripts.build_app.common import PATH_DIST, PATH_PACKAGING, require_external_tool
from scripts.build_app.innosetup import PATH_DIST_INSTALLER, ensure_installer_dist

PATH_PACKAGING_CHOCOLATEY = PATH_PACKAGING.joinpath("choco")


class ChocolateyTemplate(Template):
    delimiter = "$dynamic:"


def fill_template_file(
    template_file: Path,
    generated_nuspec: Path,
    template_filler: Mapping[str, str],
    *,
    encoding: str = "utf-8",
):
    with template_file.open(encoding=encoding) as f:
        content = f.read()

    try:
        formatted_content = ChocolateyTemplate(content).substitute(template_filler)
    except KeyError as e:
        raise KeyError(f"Missing template key in {template_file}") from e
    except ValueError as e:
        raise ValueError(f"Invalid template {template_file}") from e

    with generated_nuspec.open(mode="w", encoding=encoding) as f:
        f.write(formatted_content)


def file_sha256(file_path: Path, block_size: int = 65536):
    sha256_hash = hashlib.sha256()
    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(block_size), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


def get_chocolatey_template_filler() -> Mapping[str, str]:
    with Path("LICENSE").open(encoding="utf8") as license_file:
        license_content = license_file.read()
    with Path("README_choco.md").open(encoding="utf8") as readme_file:
        readme_content = readme_file.read()

    return {
        "display_name": app_metadata.display_name,
        "version_windows": app_version_variants.windows,
        "version_wheel": app_version_variants.wheel,
        "license_url": "https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/blob/master/LICENSE",
        "license_content": license_content,
        "repository_url": app_metadata.repository or "",
        "bug_tracker_url": app_metadata.bug_tracker or "",
        "release_url": app_metadata.bug_tracker or "",
        "author": app_metadata.author or "",
        "icon_url_cdn": "https://cdn.jsdelivr.net/gh/hellotool/VCFGeneratorLiteWithTkinter@f1f5dac3e98e9a375bc68951cade995d611bb094/assets/images/icon.svg",
        "summary": app_metadata.summary or "",
        "description": readme_content,
        "release_notes": app_metadata.release_notes or "",
        "copyright": app_metadata.copyright or "",
        "installer_sha256": file_sha256(PATH_DIST_INSTALLER),
        "installer_filename": PATH_DIST_INSTALLER.name,
    }


def get_chocolatey_template_encoding(path: Path) -> str:
    if path.name.endswith(".ps1") or path.name == "LICENSE.txt":
        return "utf-8-sig"
    return "utf-8"


@contextmanager
def prepare_chocolatey_package(template_filler: Mapping[str, str], package_dir: Path):
    tools_template_dir = package_dir / "tools-template"
    tools_generated_dir = package_dir / "tools-generated"
    template_nuspec_path = next(package_dir.glob("*.template.nuspec"))
    generated_nuspec_path = template_nuspec_path.with_stem(
        template_nuspec_path.stem[: -len(".template")] + ".generated"
    )

    if tools_generated_dir.exists():
        shutil.rmtree(tools_generated_dir)

    if tools_template_dir.exists() and tools_template_dir.is_dir():
        shutil.copytree(tools_template_dir, tools_generated_dir)

        for file_path in tools_generated_dir.rglob("*"):
            if not file_path.is_file():
                continue

            fill_template_file(
                file_path,
                file_path,
                template_filler,
                encoding=get_chocolatey_template_encoding(file_path),
            )
    else:
        tools_generated_dir.mkdir(exist_ok=True)

    if generated_nuspec_path.is_file():
        generated_nuspec_path.unlink()

    fill_template_file(template_nuspec_path, generated_nuspec_path, template_filler)

    yield generated_nuspec_path

    shutil.rmtree(tools_generated_dir)
    generated_nuspec_path.unlink()


def pack_with_chocolatey(spec_path: Path):
    choco_path = require_external_tool("choco", "Chocolatey")
    subprocess.run([choco_path, "pack", spec_path, "--output-directory", PATH_DIST.absolute()], check=True)  # noqa: S603


def build_chocolatey_packages():
    ensure_installer_dist()
    template_filler: Mapping[str, str] = get_chocolatey_template_filler()
    for package_dir in PATH_PACKAGING_CHOCOLATEY.iterdir():
        with prepare_chocolatey_package(template_filler, package_dir) as nuspec_file_path:
            pack_with_chocolatey(nuspec_file_path)
