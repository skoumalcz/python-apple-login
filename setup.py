import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='python-apple-login',
    version='0.1',
    packages=['python_apple_login'],
    description='Application for support of apple login',
    long_description=README,
    author='Jan Kotras, Libor Polehna',
    author_email='jan.kotras@skoumal.net, libor.polehna@skoumal.net',
    url='https://www.skoumal.com/',
    license='BSD License',
    python_requires='>=3.12',
    install_requires=[
        "pycryptodome==3.9.*",
        "pyjwt==2.10.*",
        "requests==2.32.*"
    ]
)
