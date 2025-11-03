from meshroom.core import desc
from meshroom.core.graph import Graph, loadGraph

from .utils import registerNodeDesc, unregisterNodeDesc


class NodeWithDynamicOutputs(desc.Node):
    inputs = [
        desc.BoolParam(
            name="boolInput",
            label="Bool Input",
            description="A boolean input.",
            value=False,
        ),
        desc.File(
            name="fileInput",
            label="File Input",
            description="A file input.",
            value="testFile",
        ),
        desc.StringParam(
            name="stringInput",
            label="String Input",
            description="A string input.",
            value="testString",
        ),
        desc.IntParam(
            name="intInput",
            label="Int Input",
            description="An integer input.",
            value=1,
        ),
        desc.FloatParam(
            name="floatInput",
            label="Float Input",
            description="A floating input.",
            value=5.0,
        ),
    ]

    outputs = [
        desc.BoolParam(
            name="boolOutput",
            label="Bool Output",
            description="A boolean output.",
            value=None,
        ),
        desc.File(
            name="fileOutput",
            label="File Output",
            description="A file Output.",
            value=None,
        ),
        desc.StringParam(
            name="stringOutput",
            label="String Output",
            description="A string output.",
            value=None,
        ),
        desc.IntParam(
            name="intOutput",
            label="Int Output",
            description="An integer output.",
            value=None,
        ),
        desc.FloatParam(
            name="floatOutput",
            label="Float Output",
            description="A floating output.",
            value=None,
        ),
    ]

    def process(self, node):
        node.boolOutput.value = not node.boolInput.value
        node.fileOutput.value = node.fileInput.value + ".ext"
        node.stringOutput.value = node.stringInput.value.upper()
        node.intOutput.value = node.intInput.value + 1
        node.floatOutput.value = node.floatInput.value * 2.0


class InputNodeWithDynamicOutputs(desc.InputNode):
    inputs = [
        desc.BoolParam(
            name="boolInput",
            label="Bool Input",
            description="A boolean input.",
            value=False,
        ),
        desc.File(
            name="fileInput",
            label="File Input",
            description="A file input.",
            value="testFile",
        ),
        desc.StringParam(
            name="stringInput",
            label="String Input",
            description="A string input.",
            value="testString",
        ),
        desc.IntParam(
            name="intInput",
            label="Int Input",
            description="An integer input.",
            value=1,
        ),
        desc.FloatParam(
            name="floatInput",
            label="Float Input",
            description="A floating input.",
            value=5.0,
        ),
    ]

    outputs = [
        desc.BoolParam(
            name="boolOutput",
            label="Bool Output",
            description="A boolean output.",
            value=None,
        ),
        desc.File(
            name="fileOutput",
            label="File Output",
            description="A file Output.",
            value=None,
        ),
        desc.StringParam(
            name="stringOutput",
            label="String Output",
            description="A string output.",
            value="",
        ),
        desc.IntParam(
            name="intOutput",
            label="Int Output",
            description="An integer output.",
            value=None,
        ),
        desc.FloatParam(
            name="floatOutput",
            label="Float Output",
            description="A floating output.",
            value=None,
        ),
    ]


class TestNodesWithDynamicOutputs:
    @classmethod
    def setup_class(cls):
        registerNodeDesc(NodeWithDynamicOutputs)
        registerNodeDesc(InputNodeWithDynamicOutputs)

    @classmethod
    def teardown_class(cls):
        unregisterNodeDesc(NodeWithDynamicOutputs)
        unregisterNodeDesc(InputNodeWithDynamicOutputs)

    def test_processWithDynamicOutputs(self, graphSavedOnDisk):
        graph: Graph = graphSavedOnDisk
        node = graph.addNewNode(NodeWithDynamicOutputs.__name__)
        node.nodeDesc.processChunk(node.chunks.at(0))

        assert node.boolOutput.value
        assert node.fileOutput.value == "testFile.ext"
        assert node.stringOutput.value == "TESTSTRING"
        assert node.intOutput.value == 2
        assert node.floatOutput.value == 10.0

    def test_loadGraphWithUncomputedDynamicOutputs(self, graphSavedOnDisk):
        graph: Graph = graphSavedOnDisk
        node = graph.addNewNode(NodeWithDynamicOutputs.__name__)
        graph.save()

        loadedGraph = loadGraph(graph.filepath)
        loadedNode = loadedGraph.node(node.name)
        assert loadedNode

        assert loadedNode.boolOutput.value is None
        assert loadedNode.fileOutput.value is None
        assert loadedNode.stringOutput.value is None
        assert loadedNode.intOutput.value is None
        assert loadedNode.floatOutput.value is None

    def test_loadGraphWithComputedDynamicOutputs(self, graphSavedOnDisk):
        graph: Graph = graphSavedOnDisk
        node = graph.addNewNode(NodeWithDynamicOutputs.__name__)
        node.nodeDesc.processChunk(node.chunks.at(0))

        assert node.boolOutput.value
        assert node.fileOutput.value == "testFile.ext"
        assert node.stringOutput.value == "TESTSTRING"
        assert node.intOutput.value == 2
        assert node.floatOutput.value == 10.0

        graph.save()

        loadedGraph = loadGraph(graph.filepath)
        loadedNode = loadedGraph.node(node.name)
        assert loadedNode

        assert loadedNode.boolOutput.value
        assert loadedNode.fileOutput.value == "testFile.ext"
        assert loadedNode.stringOutput.value == "TESTSTRING"
        assert loadedNode.intOutput.value == 2
        assert loadedNode.floatOutput.value == 10.0
