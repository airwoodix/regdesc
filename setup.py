from setuptools import setup

setup(
    name="regdesc",
    author="Etienne Wodey",
    author_email="airwoodix@posteo.me",
    description="Pythonic hardware register descriptors",
    license="GPLv3",
    use_scm_version=True,
    packages=["regdesc", "regdesc.devices"],
    test_suite="regdesc.tests",
)
