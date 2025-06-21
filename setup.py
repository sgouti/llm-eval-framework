from setuptools import setup, find_packages

setup(
   name="llm-eval-framework",
       version="0.1.0",
       packages=find_packages(where="src"),
       package_dir={"": "src"},
       install_requires=[
           "streamlit",
           "pandas",
           "boto3",
           "ollama",
           "deepeval",
           "pyyaml"
       ],
       extras_require={
           "dev": ["pytest", "pytest-mock", "pytest-cov", "streamlit-testing"]
       }
)