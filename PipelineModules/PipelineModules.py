import os
import slicer
from PipelineCreator import PipelineCreatorLogic
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin

#import all the default wrappings. doing the import will register them with the pipeline creator
from PipelineModulesLib import (
  PipelineParameters,
  SegmentationsWrapping,
  SegmentEditorWrapping,
  SurfaceToolboxWrapping,
  vtkFilterJSONReader,
)

#
# PipelineModules
#

class PipelineModules(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "Pipeline Modules"
    self.parent.categories = ["Pipelines"]
    self.parent.dependencies = ["PipelineCreator", "SegmentEditor"]  # TODO: add here list of module names that this module requires
    self.parent.contributors = ["Connor Bowley (Kitware, Inc.)"]
    # TODO: update with short description of the module and a link to online module documentation
    self.parent.helpText = """
This module exists to create pipelines for the PipelineCreator to use.
"""
    self.parent.acknowledgementText = ""

#
# PipelineModulesWidget
#

class PipelineModulesWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent=None):
    """
    Called when the user opens the module the first time and the widget is initialized.
    """
    ScriptedLoadableModuleWidget.__init__(self, parent)
    VTKObservationMixin.__init__(self)  # needed for parameter node observation
    self.logic = None

  def setup(self):
    """
    Called when the user opens the module the first time and the widget is initialized.
    """
    ScriptedLoadableModuleWidget.setup(self)

    # Load widget from .ui file (created by Qt Designer).
    # Additional widgets can be instantiated manually and added to self.layout.
    uiWidget = slicer.util.loadUI(self.resourcePath('UI/PipelineModules.ui'))
    self.layout.addWidget(uiWidget)
    self.ui = slicer.util.childWidgetVariables(uiWidget)

    # Set scene in MRML widgets. Make sure that in Qt designer the top-level qMRMLWidget's
    # "mrmlSceneChanged(vtkMRMLScene*)" signal in is connected to each MRML widget's.
    # "setMRMLScene(vtkMRMLScene*)" slot.
    uiWidget.setMRMLScene(slicer.mrmlScene)

    # Create logic class. Logic implements all computations that should be possible to run
    # in batch mode, without a graphical user interface.
    self.logic = PipelineModulesLogic()

    # Connections

    # These connections ensure that we update parameter node when scene is closed
    self.addObserver(slicer.mrmlScene, slicer.mrmlScene.StartCloseEvent, self.onSceneStartClose)
    self.addObserver(slicer.mrmlScene, slicer.mrmlScene.EndCloseEvent, self.onSceneEndClose)

#
# PipelineModulesLogic
#

class PipelineModulesLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def loadVTKJSON(self, pipelineCreatorLogic):
    vtkFilterJSONReader.RegisterPipelineModules(pipelineCreatorLogic, self.resourcePath('PipelineVTKFilterJSON'))

  def resourcePath(self, filename):
    scriptedModulesPath = os.path.dirname(slicer.util.modulePath(self.moduleName))
    return os.path.join(scriptedModulesPath, 'Resources', filename)

  def __init__(self):
    """
    Called when the logic class is instantiated. Can be used for initializing member variables.
    """
    ScriptedLoadableModuleLogic.__init__(self)

#
# PipelineModulesTest
#

class PipelineModulesTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear()

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_PipelineModules1()

  def test_PipelineModules1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """
    #TODO: tests for pipelines created by this module
    pass

#load the vtk json files when able
try:
  slicer.modules.pipelinemodules
  PipelineModulesLogic().loadVTKJSON(PipelineCreatorLogic()) #this will throw if pipelinecreator has not been loaded yet
except AttributeError:
  def callback(moduleName):
    if "PipelineModules" == moduleName:
      PipelineModulesLogic().loadVTKJSON(PipelineCreatorLogic())
  slicer.app.moduleManager().moduleLoaded.connect(callback)
