#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys
from os.path import dirname, abspath, join
import unittest
root_path = abspath(join(dirname(__file__), "../../"))
sys.path.insert(0, root_path)

from tests.base.base_functional_test import BaseFunctionalTest
from skink.models import Pipeline, PipelineItem, Project
from skink.repositories import PipelineRepository

class TestPipelineRepository(BaseFunctionalTest):

    def test_create_pipeline(self):
        projecta = self.create_project()
        projectb = self.create_project(name=u"ProjectB")

        repository = PipelineRepository()
        created_pipeline = repository.create(name=u"Test Pipeline", pipeline_definition=u"ProjectA > ProjectB")
        
        pipeline = repository.get(created_pipeline.id)
        
        self.assertEqual(pipeline.name, u"Test Pipeline")
        self.assertEqual(len(pipeline.items), 2)
        self.assertNotEqual(pipeline.items[0].project, None)
        self.assertNotEqual(pipeline.items[1].project, None)
        self.assertEqual(pipeline.items[0].project.id, projecta.id)
        self.assertEqual(pipeline.items[1].project.id, projectb.id)
        self.assertEqual(str(pipeline), "ProjectA > ProjectB")

    def test_update_pipeline(self):
        projecta = self.create_project(name=u"A")
        projectb = self.create_project(name=u"B")
        projectc = self.create_project(name=u"C")

        repository = PipelineRepository()
        created_pipeline = repository.create(name=u"Test Pipeline", pipeline_definition=u"A > B")
        
        repository.update(created_pipeline.id, name=u"Updated Pipeline", pipeline_definition=u"B > A > C")
        
        pipeline = repository.get(created_pipeline.id)
        
        self.assertEqual(pipeline.name, u"Updated Pipeline")
        self.assertEqual(len(pipeline.items), 3)
        self.assertNotEqual(pipeline.items[0].project, None)
        self.assertNotEqual(pipeline.items[1].project, None)
        self.assertNotEqual(pipeline.items[2].project, None)
        self.assertEqual(pipeline.items[0].project.id, projectb.id)
        self.assertEqual(pipeline.items[1].project.id, projecta.id)
        self.assertEqual(pipeline.items[2].project.id, projectc.id)
        self.assertEqual(str(pipeline), "B > A > C")
        
    def test_get_all_pipelines(self):
        projecta = self.create_project()
        projectb = self.create_project(name=u"ProjectB")
        projectc = self.create_project(name=u"ProjectC")

        repository = PipelineRepository()
        created_pipeline = repository.create(name=u"Test Pipeline", pipeline_definition=u"ProjectA > ProjectB")
        created_pipeline2 = repository.create(name=u"Test Pipeline 2", pipeline_definition=u"ProjectB > ProjectA > ProjectC")
        
        pipelines = repository.get_all()
        
        self.assertEqual(len(pipelines), 2)
        self.assertEqual(pipelines[0].name, u"Test Pipeline")
        self.assertEqual(pipelines[1].name, u"Test Pipeline 2")
        self.assertEqual(len(pipelines[0].items), 2)
        self.assertEqual(len(pipelines[1].items), 3)

        self.assertNotEqual(pipelines[0].items[0].project, None)
        self.assertNotEqual(pipelines[0].items[1].project, None)
        self.assertEqual(pipelines[0].items[0].project.id, projecta.id)
        self.assertEqual(pipelines[0].items[1].project.id, projectb.id)
        
        self.assertNotEqual(pipelines[1].items[0].project, None)
        self.assertNotEqual(pipelines[1].items[1].project, None)
        self.assertNotEqual(pipelines[1].items[2].project, None)
        self.assertEqual(pipelines[1].items[0].project.id, projectb.id)
        self.assertEqual(pipelines[1].items[1].project.id, projecta.id)
        self.assertEqual(pipelines[1].items[2].project.id, projectc.id)

    def test_delete_pipeline(self):
        projecta = self.create_project()
        projectb = self.create_project(name=u"ProjectB")

        repository = PipelineRepository()
        created_pipeline = repository.create(name=u"Test Pipeline", pipeline_definition=u"ProjectA > ProjectB")
        
        repository.delete(created_pipeline.id)
        
        pipelines = repository.get_all()
        self.assertEqual(len(pipelines), 0)
        
    def test_get_all_pipelines_for_project(self):
        projecta = self.create_project()
        projectb = self.create_project(name=u"ProjectB")
        projectc = self.create_project(name=u"ProjectC")

        repository = PipelineRepository()
        created_pipeline = repository.create(name=u"Test Pipeline", pipeline_definition=u"ProjectA > ProjectB")
        created_pipeline2 = repository.create(name=u"Test Pipeline 2", pipeline_definition=u"ProjectB > ProjectA > ProjectC")
        
        pipelines = repository.get_all_pipelines_for(projectc)
        
        self.assertEqual(len(pipelines), 1)
        self.assertEqual(pipelines[0].name, u"Test Pipeline 2")
        self.assertEqual(len(pipelines[0].items), 3)
        
if __name__ == '__main__':
    unittest.main()
