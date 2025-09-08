Package Setup
=============

Short tutorial on how to create and configure a new ROS Package.

Creating a Package
------------------

Use the following command to create a C/C++ package or a Python Package:

.. code:: bash
    ros2 pkg create --build-type ament_cmake <Package Name>

It is easier to use ament_cmake for installing python packages because
ament_python has a poorly formated config.
