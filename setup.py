from setuptools import setup, find_packages

requirements = [
    "pillow ~= 9.1.1"
]


setup(
    name="braillert",
    version="2.1.7",
    packages=find_packages("src"),
    package_dir={'': "src"},
    include_package_data=True,
    author="ov3rwrite",
    author_email="ilyabelykh123@gmail.com",
    install_requires = requirements,
    url="https://github.com/ov3rwrite/braillert",
    license="MIT",
    entry_points = {
        'console_scripts': [
            'braillert = braillert.main:main',
        ],
    }
)
