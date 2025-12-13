from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Avg
from .models import Campaign, Metric
from .serializers import CampaignSerializer


class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'platform', 'status']
    ordering_fields = ['created_at', 'name', 'status']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def active(self, request):
        active_campaigns = Campaign.objects.filter(status='active')
        serializer = self.get_serializer(active_campaigns, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def pause(self, request, pk=None):
        campaign = self.get_object()
        campaign.status = 'paused'
        campaign.save()
        serializer = self.get_serializer(campaign)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def resume(self, request, pk=None):
        campaign = self.get_object()
        campaign.status = 'active'
        campaign.save()
        serializer = self.get_serializer(campaign)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        campaign = self.get_object()
        campaign.pk = None
        campaign.id = None
        campaign.name = f"{campaign.name} (Copy)"
        campaign.save()
        serializer = self.get_serializer(campaign)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        campaigns = Campaign.objects.all()
        metrics = Metric.objects.all()

        total_impressions = metrics.aggregate(Sum('impressions'))['impressions__sum'] or 0
        total_clicks = metrics.aggregate(Sum('clicks'))['clicks__sum'] or 0
        total_engagements = metrics.aggregate(Sum('engagements'))['engagements__sum'] or 0
        total_conversions = metrics.aggregate(Sum('conversions'))['conversions__sum'] or 0
        total_spend = metrics.aggregate(Sum('spend'))['spend__sum'] or 0

        avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        avg_engagement_rate = (total_engagements / total_impressions * 100) if total_impressions > 0 else 0
        conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
        roi = ((total_conversions * 100 - total_spend) / total_spend * 100) if total_spend > 0 else 0

        return Response({
            'total_campaigns': campaigns.count(),
            'active_campaigns': campaigns.filter(status='active').count(),
            'total_impressions': total_impressions,
            'total_clicks': total_clicks,
            'total_engagements': total_engagements,
            'total_conversions': total_conversions,
            'total_spend': float(total_spend),
            'avg_ctr': round(avg_ctr, 2),
            'avg_engagement_rate': round(avg_engagement_rate, 2),
            'conversion_rate': round(conversion_rate, 2),
            'roi': round(roi, 2),
        })

    @action(detail=False, methods=['get'])
    def platform_performance(self, request):
        platforms = Campaign.objects.values('platform').distinct()
        platform_stats = []

        for platform in platforms:
            platform_name = platform['platform']
            campaigns = Campaign.objects.filter(platform=platform_name)
            metrics = Metric.objects.filter(campaign__in=campaigns)

            impressions = metrics.aggregate(Sum('impressions'))['impressions__sum'] or 0
            clicks = metrics.aggregate(Sum('clicks'))['clicks__sum'] or 0
            engagements = metrics.aggregate(Sum('engagements'))['engagements__sum'] or 0
            conversions = metrics.aggregate(Sum('conversions'))['conversions__sum'] or 0
            spend = metrics.aggregate(Sum('spend'))['spend__sum'] or 0

            ctr = (clicks / impressions * 100) if impressions > 0 else 0
            engagement_rate = (engagements / impressions * 100) if impressions > 0 else 0
            conversion_rate = (conversions / clicks * 100) if clicks > 0 else 0
            cpc = (spend / clicks) if clicks > 0 else 0

            platform_stats.append({
                'platform': platform_name,
                'campaigns_count': campaigns.count(),
                'total_impressions': impressions,
                'total_clicks': clicks,
                'total_engagements': engagements,
                'total_conversions': conversions,
                'total_spend': float(spend),
                'ctr': round(ctr, 2),
                'engagement_rate': round(engagement_rate, 2),
                'conversion_rate': round(conversion_rate, 2),
                'cpc': round(cpc, 2),
            })

        return Response(platform_stats)
