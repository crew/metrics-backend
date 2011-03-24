============
flamongo-key
============

``flamongo-key`` is a command to create namespaces and apikeys.

Create a Namespace
------------------

.. code-block:: bash

    flamongo-key --namespace <namespace> --create-namespace --database <database>

::

    <namespace> := Short string
    <database>  := Short string

Create an Apikey
----------------

.. code-block:: bash

    flamongo-key --namespace <namespace> --create <access>

::

    <access> := 'r' | 'rw' | 'w'

List the Apikeys
----------------

.. code-block:: bash

    flamongo-key --namespace <namespace> --list

Prints something like::

    e2901967-42df-4175-ae75-7d55041ab6f3    rw
    b1a592a7-380e-4281-ae58-5a3104c75dd0    r

Delete an apikey
----------------

.. code-block:: bash

    flamongo-key --namespace <namespace> --delete b1a592a7-380e-4281-ae58-5a3104c75dd0
