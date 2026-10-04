from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="blofin",
    version="0.1.0",
    description="Python SDK for the BloFin perpetual-futures exchange API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # Explicitly ship the blofin package. find_packages() only discovers
    # directories containing __init__.py, so an explicit list guarantees the
    # modules are packaged rather than silently producing an empty wheel.
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        # 10.x is required for the asyncio client; the SDK relies on
        # websockets.connect() and its State enum, both present since 10.0.
        "websockets>=10.0",
    ],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
