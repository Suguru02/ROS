from glob import glob

from setuptools import find_packages, setup

package_name = 'course_description'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch',
            glob('launch/*.launch.py')),
        ('share/' + package_name + '/urdf',
            glob('urdf/*.urdf.xacro')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Haruto',
    maintainer_email='haruto@example.com',
    description='Robot description for PR06',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
        ],
    },
)
