=====
GoMechanic Starter
=====

GMLogging
-----------

1. Add "gmlogging" to your INSTALLED_APPS setting like this::

    ```
    INSTALLED_APPS = [
        ...
        'gmlogging',
    ]
    ```

2. Initialize in your settings.py like this::

    ```
    import gmlogging
    gm_logging = gmlogging.GMLogging("name of your project")
    ```

3. Use gm_logging.print instead of python print like this::
   
    ```
    import settings
    gm_logging.print("1", 2, 3.0, {"4" : "5"}, [6,7], ["8", "9"])
    ```