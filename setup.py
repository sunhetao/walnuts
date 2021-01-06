from setuptools import setup, find_packages

setup(
    name="walnuts",
    version="0.0.7",
    keywords=("api test", "automation", "testing", "walnut"),
    description="api test tools",
    long_description="simplify api testing",
    url="https://github.com/sunhetao/walnuts",
    author="sunhetao",
    author_email="s13183036086@gmail.com",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    platforms="any",
    install_requires=['requests', 'configobj', 'pyyaml', 'click', 'jinja2', 'pytest', 'pytest-html'],
    entry_points='''
    [console_scripts]
    walnuts=walnuts.cli:walnuts_cli
    '''
)
