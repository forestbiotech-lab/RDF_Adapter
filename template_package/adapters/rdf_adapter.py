from rdflib import Literal
import random
import string
from enum import Enum, auto
from itertools import chain
from typing import Optional
from biocypher._logger import logger


logger.debug(f"Loading module {__name__}.")



class AdapterNodeProperties(Enum):
    """
    Enum for the node properties
    """
    hasName = "name"
    hasDescription = "description"
    hasIdentifier = "identifier"
    hasInternalIdentifier = "internal identifier"
    hasExternalIdentifier = "external identifier"
    hasMIAPPEVersion = "version of MIAPPE"
    hasAssociatedPublication = "associated publication"
    hasAbbreviation = "abbreviation"
    hasStartDateTime = "start date time"
    hasEndDateTime = "end date time"
    hasCulturalPractices = "cultural practices"
    hasObservationUnitDescription = "observation unit description"
    hasGenus = "genus"
    hasSpecies = "species"
    hasMaterialIdentifier = "material identifier"
    hasTaxonIdentifier = "taxon identifier"
    hasPlantAnatomicalEntity = "plant anatomical entity"
    hasPlantStructureDevelopmentStage = "plant structural development stage"

class AdapterEdgeType(Enum):
    """
    Enum for the types of the protein adapter.
    """

    hasPart = "has part"
    partOf = "part of"
    hasBiologicalMaterial = "has biological material"
    derivesFrom = "derives from"
    hasTrait = "has trait"
    hasVariable = "has variable"



class RDF_Adapter:
    """
    Example BioCypher adapter. Generates nodes and edges for creating a
    knowledge graph.

    Args:
        node_types: List of node types to include in the result.
        node_fields: List of node fields to include in the result.
        edge_types: List of edge types to include in the result.
        edge_fields: List of edge fields to include in the result.
    """

    def __init__(
        self,
        triples,
    ):
        self.nodes = {}
        self.triples = triples


    def get_nodes(self):
        """
        Returns a generator of node tuples for node types specified in the
        adapter constructor.
        """

        logger.info("Generating nodes.")


        ## The class names are defined as owl terms

        #for node in self.get_classes_by_name("investigation"):
        #    self.nodes[node.id] = node
        #    yield node.id, "investigation", node.properties

        #for node in self.get_classes_by_name("study"):
        #    self.nodes[node.id] = node
        #    yield node.id, "study", node.properties

        for n in ["investigation", "study", "biological_material", "observation_unit", "observed_variable", "trait", "sample"]:
            label = n
            if len(n.split("_")) == 2:
                label = n.replace("_", " ")
            for node in self.get_classes_by_name(n):
                self.nodes[node.id] = node
                yield node.id, label, node.properties

        #for node in self.get_classes_by_name("biological_material"):
        #   self.nodes[node.id] = node
        #   yield node.id, "biological material", node.properties

        #for node in self.get_classes_by_name("observation_unit"):
        #    self.nodes[node.id] = node
        #    yield node.id, "observationUnit", node.properties

        #for node in self.get_classes_by_name("observed_variable"):
        #    self.nodes[node.id] = node
        #    yield node.id, "observedVariable", node.properties




        #for subj, pred, obj in self.triples:
        #    # TODO  Check if node is a data property
        #    # Create IDs
        #    # Properties
        #    self.nodes.append(Node(subj, subj))
        #    self.nodes.append(Node(obj, obj))

        #for node in self.nodes:
        #    yield node.get_id(), node.get_label(), node.get_properties()

        #if ExampleAdapterNodeType.PROTEIN in self.node_types:
        #    [self.nodes.append(Protein(fields=self.node_fields)) for _ in range(100)]
        #
        #if ExampleAdapterNodeType.DISEASE in self.node_types:
        #    [self.nodes.append(Disease(fields=self.node_fields)) for _ in range(100)]
        #
        #for node in self.nodes:
        #    yield (node.get_id(), node.get_label(), node.get_properties())


    def get_edges(self):
        """
        Returns a generator of edge tuples for edge types specified in the
        adapter constructor.

        Args:
            probability: Probability of generating an edge between two nodes.
        """

        logger.info("Generating edges.")

        if not self.nodes:
            raise ValueError("No nodes found. Please run get_nodes() first.")

        #for subj, pred, obj in self.triples:
            #TODO
            # IF SUBJ and obj are Classes

        for node in self.nodes:
            query_properties = f"""
                        SELECT ?pred ?obj
                        WHERE {{
                            <{node}> ?pred ?obj . 
                        }}
                        """
            results_prop_query = self.triples.query(query_properties)
            for predicate, observation in results_prop_query:
                if not self.is_literal(observation):
                    if observation in self.nodes:
                        edge = predicate.split("#")[-1]
                        edge_type = AdapterEdgeType[edge].value
                        yield (
                            None,
                            self.nodes[node].id,
                            self.nodes[observation].id,
                            edge_type,
                            {},
                        )

    def get_classes_by_name(self, name):
        query = f"""
            SELECT ?subject
            WHERE {{
                ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/ppeo/PPEO.owl#{name}> . 
            }}
            """

        # Execute the query
        results = self.triples.query(query)

        # Print the filtered subjects

        for row in results:
            properties = {}
            subject = row[0]
            query_properties = f"""
            SELECT ?pred ?obj
            WHERE {{
                <{subject}> ?pred ?obj . 
            }}
            """
            results_prop_query = self.triples.query(query_properties)
            for property_row in results_prop_query:
                if self.is_literal(property_row[1]):
                    try:
                        prop_key = AdapterNodeProperties[property_row[0].split("#")[-1]].value
                        properties[prop_key] = property_row[1]
                    finally:
                        continue



            yield Node(row[0], row[0].split("/")[-1], properties)

    def is_literal(self, observation):
        return isinstance(observation, Literal)

    def get_node_count(self):
        """
        Returns the number of nodes generated by the adapter.
        """
        return len(list(self.get_nodes()))






class Node:
    """
    Base class for nodes.
    """

    def __init__(self, id, label, properties):
        self.id = id
        self.label = label
        self.properties = properties

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



class Investigation(Node):
    """
    Generates instances of proteins.
    """
    def __init__(self, triples):
        self.fields = fields
        self.id = self._generate_id()
        self.label = "Investigation"
        self.properties = self._generate_properties()

    query = """
    SELECT
    WHERE {
        ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/ppeo/PPEO.owl#investigation> . 
    }
    """

    # Execute the query
    #results = triples.query(query)

    # Print the filtered subjects
    #for row in results:
    #    print(row[0])


class Protein(Node):
    """
    Generates instances of proteins.
    """

    def __init__(self):
        self.id = self._generate_id()
        self.label = "uniprot_protein"
        self.properties = self._generate_properties()

    def _generate_id(self):
        """
        Generate a random UniProt-style id.
        """
        lets = [random.choice(string.ascii_uppercase) for _ in range(3)]
        nums = [random.choice(string.digits) for _ in range(3)]

        # join alternating between lets and nums
        return "".join([x for y in zip(lets, nums) for x in y])

    def _generate_properties(self):
        properties = {}

        ## random amino acid sequence
        if (
            self.fields is not None
            and ExampleAdapterProteinField.SEQUENCE in self.fields
        ):
            # random int between 50 and 250
            l = random.randint(50, 250)

            properties["sequence"] = "".join(
                [random.choice("ACDEFGHIKLMNPQRSTVWY") for _ in range(l)],
            )

        ## random description
        if (
            self.fields is not None
            and ExampleAdapterProteinField.DESCRIPTION in self.fields
        ):
            properties["description"] = " ".join(
                [random.choice(string.ascii_lowercase) for _ in range(10)],
            )

        ## taxon
        if self.fields is not None and ExampleAdapterProteinField.TAXON in self.fields:
            properties["taxon"] = "9606"

        return properties


class Disease(Node):
    """
    Generates instances of diseases.
    """

    def __init__(self, fields: Optional[list] = None):
        self.fields = fields
        self.id = self._generate_id()
        self.label = "do_disease"
        self.properties = self._generate_properties()

    def _generate_id(self):
        """
        Generate a random disease id.
        """
        nums = [random.choice(string.digits) for _ in range(8)]

        return f"DOID:{''.join(nums)}"

    def _generate_properties(self):
        properties = {}

        ## random name
        if self.fields is not None and ExampleAdapterDiseaseField.NAME in self.fields:
            properties["name"] = " ".join(
                [random.choice(string.ascii_lowercase) for _ in range(10)],
            )

        ## random description
        if (
            self.fields is not None
            and ExampleAdapterDiseaseField.DESCRIPTION in self.fields
        ):
            properties["description"] = " ".join(
                [random.choice(string.ascii_lowercase) for _ in range(10)],
            )

        return properties
