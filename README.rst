=====
GoMechanic Starter
=====

Add "gmlogging" to your INSTALLED_APPS setting like this::


    INSTALLED_APPS = [
        ...
        'gmstarter',
    ]


GMLogging
-----------

1. Initialize in your settings.py like this::


    from gmstarter.gmlogging import GMLogging
    gm_logging = GMLogging(SITE_NAME)


2. Use gm_logging.print instead of python print like this::
   

    import settings
    gm_logging.print("1", 2, 3.0, {"4" : "5"}, [6,7], ["8", "9"])


GMAPILogging
-----------

1. Add the middleware to your settings.py like this::


    MIDDLEWARE = [
        ...
        'gmstarter.gmapilogging.middleware.request_logger.GMLoggerMiddleware'
    ]
