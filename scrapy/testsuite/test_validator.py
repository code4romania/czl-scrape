import pytest
from scrapy.exceptions import DropItem
from czlscrape.items import Publication
from czlscrape.pipelines import PublicationValidatorPipeline

def create_publication():
    return Publication(
        identifier='aa',
        title="the good publication",
        institution='foo',
        description="this is a publication that has all required fields",
        type='HG',
        date='2017-04-03',
        documents=[
            {'type': 'something', 'url': 'http://example.com/something.pdf'},
        ],
    )

def test_ok():
    pipeline = PublicationValidatorPipeline()
    pipeline.process_item(create_publication(), None)

@pytest.mark.parametrize('field', [
    'identifier',
    'title',
    'institution',
    'description',
    'type',
    'date',
])
def test_missing_field(field):
    publication = create_publication()
    del publication[field]
    pipeline = PublicationValidatorPipeline()
    with pytest.raises(DropItem) as err:
        pipeline.process_item(publication, None)
