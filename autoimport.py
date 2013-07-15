# coding: utf-8
"""
AutoImport - small and simple module to handle
automatic imports of templates and urls to
django settings.

Usage:

    from autoimport import Collector
    Collector().go()

if you want to exclude some modules, use:

    Collector(exclude=('vk_api', 'secret')).go()
"""
import os
import imp
from django.conf import settings


class Collector(object):
    TEMPLATES = 'templates'
    URLS = 'urls.py'

    def __init__(self, exclude=None):
        if not exclude:
            exclude = ()

        # exclude applications
        self.exclude_apps = exclude
        self.run_directory = os.getcwd()

    def collect_templates(self, apps_list):
        """
        Collect template directories from all installed applications
        """
        ret = []

        for app in apps_list:
            if app in self.exclude_apps:
                continue

            hierarchy = app.strip().split('.')
            module_name, hierarchy = hierarchy[-1], hierarchy[:-1]

            mm = None
            try:
                mm = imp.find_module(module_name, hierarchy)
            except ImportError:
                # then it's just not in our project
                pass

            if mm:
                m_file, m_pathname, m_descr = mm

                template_dir = os.path.abspath(
                    os.path.join(
                        self.run_directory, m_pathname, Collector.TEMPLATES
                    )
                )
                if not os.path.isdir(template_dir):
                    template_dir = None

                urls = os.path.abspath(
                    os.path.join(m_pathname, Collector.URLS)
                )
                if not os.path.isfile(urls):
                    urls = None

                if template_dir or urls:
                    ret.append(
                        (template_dir, urls, mm)
                    )

        return ret

    def go(self):
        """
        Main method
        """
        full_add = self.collect_templates(settings.INSTALLED_APPS)

        new_templatedirs = filter(lambda x: x, [x[0] for x in full_add])

        # update TEMPLATE_DIRS
        new_dirs = list(settings.TEMPLATE_DIRS)
        new_dirs.extend(new_templatedirs)
        setattr(settings, 'TEMPLATE_DIRS', tuple(new_dirs))
