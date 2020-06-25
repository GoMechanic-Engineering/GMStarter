from setuptools import setup

# long_description = ('The Firebase Admin Python SDK enables server-side (backend) Python developers '
#                     'to integrate Firebase into their services and applications.')
install_requires = [
    'requests==2.22.0',
    'confluent-kafka',
    'zeep==3.4.0',
    'jsonschema==3.2.0'
]

setup(
    name="GMStarter",
    version="1.1",
    description='GMStarter Pack',
    long_description="GMStarter Pack for GoMechanic Python installations",
    url="https://github.com/GoMechanic-Engineering/GMStarter",
    author="Ashish Yadav, Prasenjit Singh",
    license="BSD-3-Clause",
    keywords='gomechanic',
    install_requires=install_requires,
    packages=['gmstarter'],
    python_requires='>=3.5',
    classifiers=[
        # 'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment'
        'Framework :: Django',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)