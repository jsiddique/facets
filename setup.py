from setuptools import setup

pkg_data = {'': ['facets/facets-jupyter.html', 'facets/base.html']}
pkgs = ['facets',]

setup(
    name='facets',
    version='0.2',
    author='J. Siddique and D. Lewis',
    url='https://github.com/jsiddique/facets',
    author_email='bi@geotab.com',
    description=("""An extension of the facets tool for machine learning"""),
    license="MIT",
    zip_safe=False,
    include_package_data=True,
    package_data=pkg_data,
    packages=pkgs,
    install_requires=["pandas", "numpy", "IPython"]
)
