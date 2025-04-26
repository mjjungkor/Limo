from setuptools import find_packages, setup

package_name = 'hello_ros2'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='mjjung',
    maintainer_email='mjjungkor@naver.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'hello_ros=hello_ros2.hello_ros:main',
            'simple_service_server=hello_ros2.simple_service_server:main'
        ],
    },
)
