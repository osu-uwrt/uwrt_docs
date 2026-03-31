#####################
Documenting a Package
#####################

To generate documentation for a package a **riptide-docs.yaml** file must be created at the root of the package. The documentation process for each language is outlined below.

****************************
**riptide-docs.yaml** Schema
****************************

.. code-block:: yaml

    type: object
    properties:
        sources:
            type: list
            description: Header and Source File Locations
            items:
                type: string

*****************************
**riptide-docs.yaml** Example
*****************************

The sources locations are relative to the package root (**riptide-docs.yaml** file location).

.. code-block:: yaml

    sources:
        - include
        - src

*********************
C / CPP Documentation
*********************

C / C++ Documentation is generated from documentation comments using Doxygen. The documentation comment in the implementation file (.c / .cpp) should include implementation details such as design considerations and implemenation details. Documentation comments in the header files (.h / .hpp) should include information about the higher level architecture as well as any api documentation (ex. what parameters are / return types). For more information on using doxygen comments you should reference the `doxygen manual <https://www.doxygen.nl/manual/index.html>`_.