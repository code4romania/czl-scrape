import json
from scraper import settings


class Serializer:
  def serialize(self, article):
    _ret = dict(
      # TODO
      identifier=None,
      title=article.title,
      type=article.article_type,
      institution=settings.INSTITUTION,
      date=article.published_at.isoformat(),
      description=article.title,
      feedback_days=article.feedback_days,
      contact=article.contact,
      documents=article.documents,
    )
    return json.dumps(_ret)
