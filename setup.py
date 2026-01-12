from setuptools import setup, find_packages

setup(
    name="screenplay-generator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "langgraph>=1.0.5",
        "langchain>=1.2.3",
        "langchain-anthropic>=1.3.1",
        "langchain-google-genai>=4.1.3",
        "reportlab>=4.2.5",
        "pillow>=11.0.0",
        "requests>=2.32.3",
        "python-dotenv>=1.0.1",
        "pydantic>=2.10.3",
        "typing-extensions>=4.15.0",
        "langgraph-checkpoint-sqlite>=3.0.1",
    ],
    python_requires=">=3.11",
)
