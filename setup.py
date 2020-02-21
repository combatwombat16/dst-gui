from setuptools import setup

setup(name='dst-gui',
      version='0.1',
      description="Web based GUI for Don't Starve Togther Server Management",
      url='http://github.com/combatwombat16/dst-gui',
      author='Ben Abrams',
      author_email='combatwombat16@gmail.com',
      license='MIT',
      packages=[],
      install_requires=[
          'flask',
          'react',
          'marshmallow'
      ],
      zip_safe=False)
