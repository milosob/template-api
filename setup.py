import setuptools

if __name__ == "__main__":
    setuptools.setup(
        name="app",
        version="0.0.1",
        packages=[
            "src",
            "bin"
        ],
        url="https://github.com/milosob/template-api",
        license="MIT",
        author="milosob",
        author_email="git@milosob.com",
        description="Extensible template for creating API services with account and JWT authentication support.",
        install_requires=open(file="./requirements.txt", mode="r").read().splitlines(),
        entry_points={
            "console_scripts": [
                "app=bin.main:cli"
            ]
        }
    )
