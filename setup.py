from setuptools import setup, find_packages
import os

version = '0.2dev'

setup(name='cal.venue',
      version=version,
      description="Plone venue content type and ATEvent extension",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='plone',
      author='Johannes Raggam',
      author_email='johannes@raggam.co.at',
      url='http://github.com/thet/cal.venue',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['cal'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'archetypes.schemaextender',
          'pycountry',
          #'Products.ATCountryWidget',
          #'Products.ATVocabularyManager',
      ],
      )
