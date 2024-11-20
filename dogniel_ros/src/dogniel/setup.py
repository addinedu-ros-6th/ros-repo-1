from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'dogniel'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*')))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='addinedu',
    maintainer_email='jyj0382@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'aruco_parking = dogniel.aruco_parking:main',
            'joint_aruco = dogniel.joint_aruco:main',
            'dogniel_amcl_pose = dogniel.dogniel_amcl_pose:main',
            'aruco_data_pub = dogniel.aruco_data_pub:main',
            'queen = dogniel.queen:main'
        ],
    },
)
