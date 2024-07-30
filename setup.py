from setuptools import setup, find_packages

setup(
    name='DM_AI',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'groq',
        'python-dotenv'
    ],
)