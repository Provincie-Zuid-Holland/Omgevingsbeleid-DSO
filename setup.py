from setuptools import setup, find_packages

setup(
    name='dso',
    version='0.0.1',
    description='STOP/TPOD Publication Generator',  
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  
    author='Arvin Wijsman, Jordy Moos',
    author_email='aa.wijsman@pzh.nl, jm.moos@pzh.nl',
    url='https://github.com/Provincie-Zuid-Holland/Omgevingsbeleid-DSO',  
    license='EUPL-1.2',  
    package_dir={"": "."},
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'dso': ['templates/*', 'templates/**/*'],  # Includes all files in the templates directory
    },
    install_requires=[
        'beautifulsoup4>=4.12.2',
        'certifi>=2023.11.17',
        'click>=8.1.7',
        'jinja2>=3.1.3',
        'lxml>=5.1.0',
        'markupsafe>=2.1.3',
        'numpy>=1.26.3',
        'packaging>=23.2',
        'pathspec>=0.12.1',
        'platformdirs>=4.1.0',
        'pydantic>=1.10.13',
        'pyproj>=3.6.1',
        'roman>=4.1',
        'shapely>=2.0.2',
        'soupsieve>=2.5',
        'tomli>=2.0.1',
        'typing-extensions>=4.9.0',
    ],
    python_requires='>=3.11',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: DSO Developers',
        'License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)',
        'Programming Language :: Python :: 3.11',
    ],
    entry_points={
        # 'console_scripts': [
        #     'generate=dso.cli generate ./input/01-hello-world/main.json ./output',
        # ],
    },
)
