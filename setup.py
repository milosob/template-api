from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name="api",
        version="0.0.1",
        packages=[
            "src",
            "bin"
        ],
        url="",
        license="",
        author="",
        author_email="",
        description="",
        install_requires=open(file="./requirements.txt", mode="r").read().splitlines(),
        entry_points={
            "console_scripts": [
                "app=bin.main:cli"
            ]
        }
    )
