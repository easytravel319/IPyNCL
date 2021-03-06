from distutils.command.install import install
from distutils import log
import sys
import os
import json
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


kernel_json = {
    "argv": [sys.executable,
	     "-m", "ncl_kernel",
	     "-f", "{connection_file}"],
    "display_name": "NCL",
    "language": "ncl",
    "name": "ncl_kernel",
}


class install_with_kernelspec(install):

    def run(self):
        install.run(self)
        user = '--user' in sys.argv
        try:
            from jupyter_client.kernelspec import install_kernel_spec
        except ImportError:
            from ipykernel.kerspec import install_kernel_spec
        
        from IPython.utils.tempdir import TemporaryDirectory
        with TemporaryDirectory() as td:
            os.chmod(td, 0o755)  # Starts off as 700, not user readable
            with open(os.path.join(td, 'kernel.json'), 'w') as f:
                json.dump(kernel_json, f, sort_keys=True)
            log.info('Installing kernel spec')
            kernel_name = kernel_json['name']
            try:
                install_kernel_spec(td, kernel_name, user=user,
                                    replace=True)
            except:
                install_kernel_spec(td, kernel_name, user=not user,
                                    replace=True)


svem_flag = '--single-version-externally-managed'
if svem_flag in sys.argv:
    sys.argv.remove(svem_flag)


with open('ncl_kernel.py') as fid:
    for line in fid:
        if line.startswith('__version__'):
            version = line.strip().split()[-1][1:-1]
            break

setup(name='ncl_kernel',
      description='A NCL kernel for Jupyter/IPython',
      url="https://github.com/suvarchal/IPyNCL",
      version=version,
      author='Suvarchal Kumar Cheedela',
      author_email='suvarchal.kumar@gmail.com',
      py_modules=['ncl_kernel','nclreplwrap'],
      license="MIT",
      cmdclass={'install': install_with_kernelspec},
      install_requires=["IPython >= 3.0","ipykernel"],
      classifiers=[
          'Framework :: IPython',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: NCL :: 6.3',
          'Topic :: System :: Shells',
      ]
)
