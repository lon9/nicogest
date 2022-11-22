from setuptools import setup

setup(
    name='nicogest',
    version='1.1.1',
    description='Niconico Douga digest maker',
    author='lon9',
    url='https://github.com/lon9/nicogest',
    packages=['nicogest'],
    install_requires=[
        'beautifulsoup4==4.7.1',
        'certifi==2019.6.16',
        'chardet==3.0.4',
        'decorator==4.4.0',
        'idna==2.8',
        'imageio==2.5.0',
        'imageio-ffmpeg==0.3.0',
        'moviepy==1.0.0',
        'nndownload==1.1',
        'numpy==1.16.4',
        'Pillow==9.3.0',
        'proglog==0.1.9',
        'requests==2.22.0',
        'soupsieve==1.9.2',
        'tqdm==4.32.2',
        'urllib3==1.25.3',
        'websockets==8.0'
    ]
)
