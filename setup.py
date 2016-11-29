from setuptools import setup, find_packages

with open('./requirements.txt') as requirements_txt:
    requirements = [ line for line in requirements_txt ]


setup(
    name='impact-javascript',
    version='0.1.0',
    description='JavaScript Impact Service',
    long_description='',
    url='https://joinrebase.com',
    author='Andrew Millspaugh',
    author_email='andrew@joinrebase.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Developer Ranking and Remote Work Marketplace',
        'License :: Rebase Terms of Use (TBD!!!)',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='rebase api code2resume',
    packages=find_packages(),
    install_requires=requirements,
    extras_require=dict(),
    package_data=dict(),
    data_files=[],
    entry_points={}
)


