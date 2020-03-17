from django.db import models
from django.db.models import (
    Case,
    CharField,
    Count,
    F,
    Q,
    Value,
    When,
)


class NewsQuerySet(models.QuerySet):
    def published_news(self):
        return (
            self.prefetch_related("factcheckeropinion_set")
            .prefetch_related("expertopinion_set")
            .annotate(
                true=Count(
                    "factcheckeropinion", filter=Q(factcheckeropinion__verdict="true")
                ),
                false=Count(
                    "factcheckeropinion", filter=Q(factcheckeropinion__verdict="false")
                ),
                unidentified=Count(
                    "factcheckeropinion",
                    filter=Q(factcheckeropinion__verdict="unidentified"),
                ),
                spam_verdicts=Count(
                    "factcheckeropinion", filter=Q(factcheckeropinion__verdict="spam")
                ),
            )
            .annotate(
                current_verdict=Case(
                    When(
                        expertopinion__verdict__isnull=False,
                        then=F("expertopinion__verdict"),
                    ),
                    When(
                        (Q(true__gte=1) & Q(false__gte=1))
                        | (
                            Q(spam_verdicts=1)
                            & (Q(false__gte=1) | Q(true__gte=1))
                        )
                        | (
                            Q(unidentified__gte=1)
                            & (
                                Q(false__gte=1)
                                | Q(true__gte=1)
                                | Q(spam_verdicts=1)
                            )
                        ),
                        then=Value("dispute"),
                    ),
                    When(true__gte=2, then=Value("true")),
                    When(false__gte=2, then=Value("false")),
                    When(
                        unidentified__gte=2,
                        then=Value("unidentified"),
                    ),
                    When(spam_verdicts__gte=2, then=Value("spam")),
                    output_field=CharField(),
                    default=Value("no_verdict"),
                )
            )
            .exclude(
                current_verdict__in=[
                    "no_verdict",
                    "spam",
                    "dispute",
                ]
            )
            .exclude(
                Q(factcheckeropinion__is_duplicate=True)
                |
                Q(expertopinion__is_duplicate=True)
            )
            .exclude(deleted=True)
        )


class NewsManager(models.Manager.from_queryset(NewsQuerySet)):
    pass
