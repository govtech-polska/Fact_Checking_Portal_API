import uuid
from django.db import models
from news.managers import NewsManager
from django.utils.translation import gettext_lazy as _


class News(models.Model):
    """
    News model representing object gathered from screenshot app.
    screenshot_url: identifies image resource on AWS S3.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,)
    url = models.URLField(max_length=2000)
    screenshot_url = models.CharField(max_length=1000, blank=True)
    reporter_email = models.EmailField(blank=False)
    reported_at = models.DateTimeField(auto_now=False, auto_now_add=False)
    text = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    deleted = models.BooleanField(default=False)

    objects = NewsManager()


class OpinionBase(models.Model):
    """
    OpinionBase model is a system base representation of opinion for an corresponding News instance.
    """

    class VerdictType(models.TextChoices):
        VERIFIED_TRUE = "true", _("Verified True")
        VERIFIED_FALSE = "false", _("Verified False")
        SPAM = "spam", _("Verified Spam")
        CANNOT_BE_VERIFIED = "unidentified", _("Cannot be verified")

    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name="%(class)s_set",
        related_query_name="%(class)s",
    )
    verdict = models.CharField(
        max_length=50,
        choices=VerdictType.choices,
        default=VerdictType.CANNOT_BE_VERIFIED,
    )

    title = models.TextField(blank=False)
    comment = models.TextField(blank=True)
    confirmation_sources = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_duplicate = models.BooleanField(default=False)

    class Meta:
        abstract = True


class FactCheckerOpinion(OpinionBase):
    """
    FastCheckerOpinion model is case specific for opinion judged by user with FastChecker role in the system.
    """

    class Meta(OpinionBase.Meta):
        db_table = "fact_checker_opinion"


class ExpertOpinion(OpinionBase):
    """
    ExpertOpinion model is case specific for opinion judged by user with Expert role in the system.
    """

    class Meta(OpinionBase.Meta):
        db_table = "expert_opinion"
