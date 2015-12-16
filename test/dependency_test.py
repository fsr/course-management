import pathlib
import unittest


class TestBowerDependencies(unittest.TestCase):
    def setUp(self):
        self.bower_folder = pathlib.Path('bower_components')

    def test_all(self):
        self.assertTrue(self.bower_folder.exists())
        self.assertTrue(self.bower_folder.joinpath('jquery').exists())


class TestNodeDependencies(unittest.TestCase):
    def setUp(self):
        self.node_folder = pathlib.Path('node_modules')

    def test_all(self):
        self.assertTrue(self.node_folder.exists())


class TestVirtualEnv(unittest.TestCase):
    pass
