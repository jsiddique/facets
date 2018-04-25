from setuptools import setup

pkg_data = {'': ['*.html']}

setup(
    name='facets',
    version='0.1',
    author='J. Siddique and D. Lewis',
    url='https://github.com/jsiddique/facets',
    author_email='bi@geotab.com',
    description=("""An extension of the facets tool for machine learning"""),
    license="MIT",
    zip_safe=False,
    packages=["facets"],
    include_package_data=True,
    pkg_data=pkg_data,
    install_requires=["pandas", "numpy", "IPython"]
)
