autoimport
============

AutoImport is a small and simple module to handle
automatic imports of templates and urls to
django settings.

Usage:

    from autoimport import Collector
    Collector().go()

if you want to exclude some modules, use:

    Collector(exclude=('vk_api', 'secret')).go()
