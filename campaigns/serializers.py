from rest_framework import serializers
from .models import Campaign, Metric


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = [
            'id', 'campaign', 'date', 'impressions', 'clicks',
            'engagements', 'conversions', 'spend', 'created_at'
        ]
        read_only_fields = ['created_at']


class CampaignSerializer(serializers.ModelSerializer):
    metrics = MetricSerializer(many=True, read_only=True)

    class Meta:
        model = Campaign
        fields = [
            'id', 'name', 'description', 'platform', 'status',
            'start_date', 'end_date', 'budget', 'impressions',
            'clicks', 'conversions', 'engagement_rate',
            'created_at', 'updated_at', 'metrics'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Campaign name is required and cannot be empty.")
        return value.strip()

    def validate_budget(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Budget cannot be negative.")
        return value

    def validate(self, data):
        if data.get('end_date') and data.get('start_date'):
            if data['end_date'] < data['start_date']:
                raise serializers.ValidationError("End date must be after start date.")
        return data
