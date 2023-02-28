import keyword
import os
import pathlib
import shutil

import networkx as nx

import slicer

from _PipelineCreatorMk2.PipelineRegistrar import PipelineInfo
from _PipelineCreatorMk2.PipelineCreation import CodeGeneration

from .validation import validatePipeline

__all__ = [
    "createPipeline",
]


def _createPythonFileCode(name: str,
                          pipeline: nx.DiGraph,
                          registeredPipelines: dict[str, PipelineInfo],
                          tab: str = " " * 4):
    runFunctionName = "run"
    # from PipelineCreation.CodeGeneration.module import createModule
    module = CodeGeneration.createModule(
        name=name,
        title=name,
        categories=["PipelineModules"],
        dependencies=["PipelineCreatorMk2"],
        contributors=["Connor Bowley (Kitware, Inc)", "PipelineCreatorMk2"],
        helpText="This module was created by the PipelineCreatorMk2.",
        acknowledgementText="This module was created by the PipelineCreatorMk2.",
        tab=tab)

    logic = CodeGeneration.createLogic(
        name=f"{name}Logic",
        pipeline=pipeline,
        registeredPipelines=registeredPipelines,
        runFunctionName=runFunctionName,
        tab=tab)

    widget = CodeGeneration.createWidget(
        name=name,
        logicClassName=f"{name}Logic",
        logicRunMethodName=runFunctionName,
        pipeline=pipeline,
        tab=tab)

    imports = CodeGeneration.cleanupImports(
        "\n".join([module.imports, widget.imports, logic.imports]))
    code = "\n\n".join([module.code, widget.code, logic.code])

    header = "# This file was generated by the PipelineCreator\n"

    return header + imports + "\n\n\n" + code


def _moduleExists(name):
    return name.lower() in [m.lower() for m in slicer.app.moduleManager().modulesNames()]


def _validatePipelineName(pipelineName: str) -> None:
        """
        Validates the pipeline name is valid. Raises an exception if it is not.
        """
        errorStr = ""
        if not pipelineName.isidentifier() or keyword.iskeyword(pipelineName.lower()) or keyword.iskeyword(pipelineName):
            errorStr += f" - Module name '{pipelineName + '/' + pipelineName.lower() if pipelineName else ''}' is not a valid pipeline module name\n"
            errorStr += f"   Acceptable names start with a letter, contain only letters, numbers, and underscores, and cannot be a python keyword\n"

        if _moduleExists(pipelineName):
            errorStr += f" - Module name '{pipelineName}' already exists. Note module names are effectively case insensitive.\n"

        if errorStr:
            raise Exception(f"Error creating pipeline: \n{errorStr}")


def _validateOutputDirectory(outputDirectory: pathlib.Path) -> None:
    """
    Validates the output directory is valid. Raises an exception if it is not.
    """
    if os.path.exists(outputDirectory) and os.listdir(outputDirectory):
        raise RuntimeError(
            f"The output directory '{outputDirectory}' should be empty or not exist")

    os.makedirs(outputDirectory, exist_ok=True)


def _validateIcon(icon):
    if not os.path.exists(icon):
        raise RuntimeError(
            f"The output directory '{icon}' should be an existing file")


def createPipeline(name: str,
                   outputDirectory: pathlib.Path,
                   pipeline: nx.DiGraph,
                   registeredPipelines: dict[str, PipelineInfo],
                   icon: pathlib.Path,
                   tab: str = " " * 4) -> None:

    # error checking
    _validatePipelineName(name)
    _validateOutputDirectory(outputDirectory)
    validatePipeline(pipeline, registeredPipelines)
    _validateIcon(icon)

    # Python file
    pythonFileCode =_createPythonFileCode(name, pipeline, registeredPipelines, tab)
    with open(os.path.join(outputDirectory, f"{name}.py"), 'w') as pyfile:
        pyfile.write(pythonFileCode)

    # CMakeLists.txt
    cmakelistsCode = CodeGeneration.createCMakeLists(name)
    with open(os.path.join(outputDirectory, "CMakeLists.txt"), 'w') as pyfile:
        pyfile.write(cmakelistsCode)

    # Icon
    iconDir = os.path.join(outputDirectory, 'Resources', 'Icons')
    os.makedirs(os.path.join(outputDirectory, 'Resources', 'Icons'))
    shutil.copy(icon, os.path.join(iconDir, f"{name}.png"))