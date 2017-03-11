import json
from scraper import settings


class Serializer:
  def serialize(self, article):
    _ret = dict(
      # TODO
      identifier=article.identifier,
      title=article.title,
      type=article.article_type,
      institution=settings.INSTITUTION,
      date=article.published_at.isoformat(),
      description='no desc',
      feedback_days=article.feedback_days,
      contact=article.contact,
      documents=article.documents,
      issuer=settings.INSTITUTION,
    )
    return _ret
    # return json.dumps(_ret)
