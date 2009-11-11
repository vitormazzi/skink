#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
from unittest import TestCase
from os.path import dirname, abspath, join
root_path = abspath(join(dirname(__file__), "../../"))
sys.path.insert(0, root_path)

from skink.imports import *
from tests.imports import *
from skink.models import *
from skink.repositories import ProjectRepository

class BaseFunctionalTest(TestCase):
    def create_project(self, name="ProjectA", build_script=u"make test", scm_repository="git_repo", branch_name="master", monitor_changes=True, tabs=None):
        self.project_repository = ProjectRepository()
        return self.project_repository.create(name=name, 
                                              build_script=build_script, 
                                              scm_repository=scm_repository, 
                                              branch_name=branch_name,
                                              monitor_changes=monitor_changes, 
                                              tabs=tabs,
                                              file_locators=None)
        
    def setUp(self):
        metadata.bind = 'sqlite:///:memory:'
        metadata.bind.echo = True
        setup_all(create_tables=True)
        create_all()

    def tearDown(self):
        elixir.session.commit()
