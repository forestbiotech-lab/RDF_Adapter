import random
import string
from enum import Enum

class ProteinAdapterFields(Enum):
    """
    Enum for the fields of the protein adapter.
    """
    ID = 'id'
    SEQUENCE = 'sequence'
    DESCRIPTION = 'description'
    TAXON = 'taxon'

class Node:
    """
    Base class for nodes.

    Args:
        fields (list): List of fields to include in the node.
    """
    def __init__(self):
        self.id = None
        self.label = None
        self.properties = {}

    def get_id(self):
        """
        Returns the node id.
        """
        return self.id

    def get_label(self):
        """
        Returns the node label.
        """
        return self.label

    def get_properties(self):
        """
        Returns the node properties.
        """
        return self.properties


class Protein(Node):
    """
    Generates instances of proteins.
    """
    def __init__(self, fields: list = None):
        self.fields = fields
        self.id = self._generate_id()
        self.label = 'uniprot_protein'
        self.properties = self._generate_properties()

    def _generate_id(self):
        """
        Generate a random UniProt-style id.
        """
        lets = [random.choice(string.ascii_uppercase) for _ in range(3)]
        nums = [random.choice(string.digits) for _ in range(3)]

        # join alternating between lets and nums
        return ''.join([x for y in zip(lets, nums) for x in y])

    def _generate_properties(self):
        properties = {}

        ## random amino acid sequence
        if self.fields is not None and ProteinAdapterFields.SEQUENCE in self.fields:

            # random int between 50 and 250
            l = random.randint(50, 250)

            properties['sequence'] = ''.join(
                [random.choice('ACDEFGHIKLMNPQRSTVWY') for _ in range(l)],
            )

        ## random description
        if self.fields is not None and ProteinAdapterFields.DESCRIPTION in self.fields:
            properties['description'] = ' '.join(
                [random.choice(string.ascii_lowercase) for _ in range(10)],
            )

        ## taxon
        if self.fields is not None and ProteinAdapterFields.TAXON in self.fields:
            properties['taxon'] = '9606'

        return properties

class ProteinAdapter:
    """
    Generates protein nodes.

    Args:
        fields (list): List of fields to include in the node.
    """
    def __init__(self, fields=None):
        self.fields = fields

    def get_nodes(self):
        """
        Returns a generator of protein node tuples.
        """
        nodes = [Protein(fields=self.fields) for _ in range(100)]
        for node in nodes:
            yield (node.get_id(), node.get_label(), node.get_properties())

    def get_node_count(self):
        """
        Returns the number of nodes generated by the adapter.
        """
        return len(self.get_nodes())