from setuptools import setup, find_packages
from pathlib import Path


templates_path = Path(__file__).parent / "regdesc" / "codegen" / "templates"
templates = [p.name for p in templates_path.glob("*.tpl.*")]

setup(
    name="regdesc",
    author="Etienne Wodey",
    author_email="airwoodix@posteo.me",
    description="Pythonic hardware register descriptors",
    license="GPLv3",
    use_scm_version=True,
    packages=find_packages(),
    test_suite="regdesc.tests",
    package_data={"regdesc.codegen.templates": templates},
    entry_points={
        "console_scripts": [
            "regdesc-serialize = regdesc.codegen.ir:ep_emit_json",
            "regdesc-codegen = regdesc.codegen.template:ep_codegen",
        ],
    },
)
