from setuptools import setup, find_packages

setup(
    name = 'bmp_argb8888_to_c',
    maintainer = 'Edmund Widl',
    maintainer_email = 'edmund.widl@gmail.com',
    version = '0.1',
    platforms = [ 'any' ],
    packages = find_packages(),
    entry_points={
        'console_scripts': [
            'argb8888_to_c = bmp_argb8888_to_c.convert:argb8888_to_c',
            'argb8888_to_c_aligned = bmp_argb8888_to_c.convert:argb8888_to_c_aligned',
            'argb8888_to_c_font = bmp_argb8888_to_c.convert:argb8888_to_c_font',
        ]
    },
    description = 'Read content of bitmap file in ARGB8888 format and convert to C array.',
    license = 'BSD 3-Clause License',
    keywords = [
        'BMP',
        'ARGB8888',
        'STM32'
    ],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering'
    ],
)