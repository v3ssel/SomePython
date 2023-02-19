from setuptools import setup, Extension

setup(
    name='calculator',
    version='1.0',
    description='Basic C Calculator',
    ext_modules=[
        Extension(
            'calculator',
            sources=['calculator.c']
        )
    ]
)
