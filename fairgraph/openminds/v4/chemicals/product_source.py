"""
Structured information about the source of a chemical substance or mixture.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.chemicals import ProductSource as OMProductSource
from fairgraph import KGObject


class ProductSource(KGObject, OMProductSource):
    """
    Structured information about the source of a chemical substance or mixture.
    """

    type_ = "https://openminds.om-i.org/types/ProductSource"
    default_space = "in-depth"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "is_source_of",
            ["openminds.v4.chemicals.ChemicalMixture", "openminds.v4.chemicals.ChemicalSubstance"],
            "productSource",
            reverse="product_source",
            multiple=True,
            description="reverse of 'product_source'",
        ),
    ]
    existence_query_properties = ("product_name", "provider")

    def __init__(
        self,
        digital_identifier=None,
        identifier=None,
        is_source_of=None,
        product_name=None,
        provider=None,
        purity=None,
        id=None,
        data=None,
        space=None,
        release_status=None,
    ):
        return KGObject.__init__(
            self,
            id=id,
            space=space,
            release_status=release_status,
            data=data,
            digital_identifier=digital_identifier,
            identifier=identifier,
            is_source_of=is_source_of,
            product_name=product_name,
            provider=provider,
            purity=purity,
        )
