import random

from news.models import News, ExpertOpinion, FactCheckerOpinion, OpinionBase
from rest_framework import serializers


class ExpertOpinionSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField("get_date")

    def get_date(self, obj):
        return obj.created_at

    class Meta:
        model = ExpertOpinion
        fields = (
            "title",
            "confirmation_sources",
            "comment",
            "date",
            "verdict",
        )


class FactCheckerOpinionSerializer(ExpertOpinionSerializer):

    class Meta(ExpertOpinionSerializer.Meta):
        model = FactCheckerOpinion
        fields = ExpertOpinionSerializer.Meta.fields


class NewsSerializer(serializers.HyperlinkedModelSerializer):
    verdict = serializers.SerializerMethodField("get_veridct")
    verified_by_expert = serializers.SerializerMethodField(
        "get_expert_verdict_status")
    title = serializers.SerializerMethodField("get_title")
    text = serializers.SerializerMethodField("get_text")
    date = serializers.SerializerMethodField("get_date")

    def get_veridct(self, obj):
        return obj.current_verdict

    def get_expert_verdict_status(self, obj):
        return obj.expertopinion_set.exists()

    def get_title(self, obj):
        opinion = obj.expertopinion_set.first() or obj.factcheckeropinion_set.first()

        return opinion.title if opinion else ""

    def get_text(self, obj):
        opinion = obj.expertopinion_set.first() or obj.factcheckeropinion_set.first()

        return f"{opinion.comment[:200]}..." if opinion else ""

    def get_date(self, obj):
        return obj.created_at

    class Meta:
        model = News
        read_only = True
        fields = (
            "id",
            "url",
            "screenshot_url",
            "text",
            "reported_at",
            "verdict",
            "verified_by_expert",
            "title",
            "date",
        )


class NewsDetailSerializer(serializers.HyperlinkedModelSerializer):
    verdict = serializers.SerializerMethodField("get_veridct")
    verified_by_expert = serializers.SerializerMethodField(
        "get_expert_verdict_status")

    expert = serializers.SerializerMethodField("get_expert")
    checkers = serializers.SerializerMethodField("get_checkers")

    def get_veridct(self, obj):
        return obj.current_verdict

    def get_expert_verdict_status(self, obj):
        return obj.expertopinion_set.exists()

    def get_checkers(self, obj):
        return FactCheckerOpinionSerializer(
            obj.factcheckeropinion_set.all()[:2], many=True).data

    def get_expert(self, obj):
        return ExpertOpinionSerializer(
            obj.expertopinion_set.first()).data

    class Meta:
        model = News
        read_only = True
        fields = (
            "id",
            "url",
            "screenshot_url",
            "text",
            "reported_at",
            "verdict",
            "verified_by_expert",
            "expert",
            "checkers",
        )

