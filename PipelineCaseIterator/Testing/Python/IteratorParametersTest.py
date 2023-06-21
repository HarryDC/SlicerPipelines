import unittest
import typing
import tempfile
import csv
import os

from PipelineCaseIteratorLibrary import IteratorParameterFile


class IteratorParametersTest(unittest.TestCase):

    def setUp(self) -> None:
        self._tempDirectory = tempfile.TemporaryDirectory()

    def tearDown(self) -> None:
        self._tempDirectory.cleanup()

    def testCreateTemplate(self):
        inputParameters: dict[str, typing.Annotated] = {'param1': str, 'param2': float}
        expectedHeaders = ['param1:str', 'param2:float']
        fileName = self._tempDirectory.name + '/file.csv'

        parameters = IteratorParameterFile(inputParameters)
        parameters.createTemplate(fileName)

        with open(fileName) as file:
            reader = csv.reader(file)
            for row in reader:
                self.assertEqual(expectedHeaders, row)
                break

    def testReadParameters(self):
        inputParameters: dict[str, typing.Annotated] = {'param1': str, 'param2': float}
        expectedParameters = [{'param1': 'test1', 'param2': '1.0'}, {'param1': 'test2', 'param2': '2.0'}]
        fileName = self._tempDirectory.name + '\\file.csv'

        with open(fileName, mode='w+') as file:
            writer = csv.writer(file)
            writer.writerow(['param1', 'param2:float'])
            writer.writerow(['test1', '1.0'])
            writer.writerow(['test2', '2.0'])

        parameters = IteratorParameterFile(inputParameters)
        parametersRead = parameters.readParameters(fileName)

        self.assertEqual(expectedParameters, parametersRead)

    def testIterateParameters(self):
        inputParameters: dict[str, typing.Annotated] = {'param1': str, 'param2': float}
        expectedParameters = [{'param1': 'test1', 'param2': '1.0'}, {'param1': 'test2', 'param2': '2.0'}]
        fileName = self._tempDirectory.name + '\\file.csv'

        with open(fileName, mode='w+') as file:
            writer = csv.writer(file)
            writer.writerow(['param1', 'param2:float'])
            writer.writerow(['test1', '1.0'])
            writer.writerow(['test2', '2.0'])

        parameters = IteratorParameterFile(inputParameters)
        parameters.readParameters(fileName)

        parametersRead = []
        for parameter in parameters:
            parametersRead.append(parameter)

        self.assertEqual(expectedParameters, parametersRead)


if __name__ == '__main__':
    unittest.main()
