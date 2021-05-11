"""
Author: John Sutor
Date: May 7th, 2020

This file contains the code for the Leopardi class, from which
the functionality of the Leopardi codebase is derived

"""

import leopardi
import os
import platform
from typing import Generic
from joblib import Parallel, delayed


class Leopardi:
    """
    The base class for the Leopardi library

    Args:

    """

    def __init__(
        self,
        camera: leopardi.BlenderCamera,
        background_loader: leopardi.BackgroundLoader,
        model_loader: leopardi.ModelLoader,
        background_directory: str = "./backgrounds",
        model_directory: str = "./models",
        blender_directory: str = None,
        render_directory: str = "./renders",
        num_jobs: int = 1,
    ):

        self._work_directory = os.getcwd()
        self._model_directory = os.path.realpath(model_directory)
        self._background_directory = os.path.realpath(background_directory)
        self._render_directory = os.path.realpath(render_directory)

        # Find the Blender directory based on OS
        SYSTEM = platform.system()

        if blender_directory is None:
            # os.path.expanduser('~')
            if SYSTEM is "Windows":
                pass
            elif SYSTEM is "Linux":
                pass
            elif SYSTEM is "Darwin":
                pass
            else:
                raise Exception(
                    "Unable to locate the Blender Install. Please provide Blender's location as an argument, or install Blender if you haven't done so already."
                )
        else:
            self._blender_directory = blender_directory

        self._num_jobs = num_jobs

        self.camera = camera
        self.background_loader = background_loader
        self.model_loader = model_loader

    def render(self, n: int = 0):
        camera_settings = self.camera()
        background = self.background_loader(n)
        model = self.model_loader(n)
        print(os.path.realpath(self._render_directory))

        rf = lambda n: os.system(
            "blender -b --python "
            + self._work_directory
            + "/leopardi/_blender.py -- -wd "
            + self._work_directory
            + " - rc "
            + str(n)
            + camera_settings
            + " -m "
            + model
            + " -rd " + self._render_directory
        )

        os.chdir(self._blender_directory)

        Parallel(n_jobs=self._num_jobs, temp_folder="/tmp")(delayed(rf)(i) for i in range(n))
