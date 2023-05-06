from setuptools import setup
VERSION='0.1.0'
setup(
    name='transformgpt',
    version=VERSION,
    packages=['transformgpt'],
    author='T Savo',
    author_email="evilgenius@nefariousplan.com",
    description="A library for transforming unstructured text into structured data without context/mappings using ChatGPT.",
    keywords="openai gpt3 chatgpt nlp chatbot transformers structruing text",
    url="https://github.com/TSavo/transformgpt",
    requires=["openai"],
    py_modules=['transformgpt'],
    download_url='https://github.com/tsavo/transformgpt/tarball/{}'.format(VERSION),
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=['openai>=0.27.6'],
    scripts=['transformgpt/main.py'],
    entry_points={
        'console_scripts': ['transformgpt=transformgpt.main:main'],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'I'
        'Natural Language :: English',
        'Environment :: Console',
        'Environment :: Libraries :: Python Modules',
        'Operating System :: OS Independent',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Text Processing :: General',
        'Topic :: Utilities',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Text Processing :: General',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Text Processing :: Utilities',
        'License :: Freely Distributable',
        'License :: OSI Approved',
        'License :: OSI Approved :: MIT License'
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
   ]
)