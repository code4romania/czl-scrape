from utils import settings


class ArticleSerializer:
    @staticmethod
    def serialize(article):
        return dict(
            # TODO
            identifier=article.identifier,
            title=article.title,
            type=article.article_type,
            institution=settings.INSTITUTION,
            date=article.published_at.isoformat(),
            description='N\A',
            feedback_days=article.feedback_days,
            contact=article.contact,
            documents=article.documents,
        )

    @staticmethod
    def is_valid(article):
        """Checks if an Article is valid, according to the API specs.
        :param article: The Article instance to validate
        :return: True or False
        """
        for field in settings.MANDATORY_FIELDS:
            if not getattr(article, field):
                return False
        return True
