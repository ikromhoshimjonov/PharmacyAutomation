from datetime import timedelta
from django.db.models import Sum, F, DecimalField, Q
from django.db.models import Sum
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.utils import timezone

from medicines.models import Medicines, Stock, Suppliers, CustomerMedicine
from medicines.serializers import MedModelSerializer, StockModelSerializer, MedicModelSerializer, SupModelSerializer, \
    CustomerModelSerializer
from rest_framework import filters



@extend_schema(tags=["med"],summary="Dori darmonlarni qushish va uchirish")
class MedModelViewSet(ModelViewSet):
    queryset = Medicines.objects.all()
    serializer_class = MedModelSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class CustomListApiView(ListAPIView):
    queryset = CustomerMedicine.objects.all()
    serializer_class = CustomerModelSerializer


@extend_schema(tags=["statistic"])
class ExpiringMedicinesView(APIView):
    def get(self, request):
        today = timezone.now().date()
        threshold_date = today + timedelta(days=90)
        count = Medicines.objects.filter(
            expiry_date__gte=today,
            expiry_date__lte=threshold_date,
            is_active=True
        ).count()
        if count:
            return Response({"expiring_count": count})
        return Response({"expiring_count": 0})

@extend_schema(tags=["statistic"])
class ExpiredProductsCountView(APIView):
    def get(self, request):
        unique_types = Medicines.objects.filter(is_active=True).count()
        return Response({"total_count": unique_types})

@extend_schema(tags=["statistic"])
class TodaySalesSummaryView(APIView):
    def get(self,request):
            today = timezone.now().date()

            query_set = Stock.objects.filter(
                date__date=today,
                type="out",
            )

            stats = query_set.aggregate(
                jami_sotuv=Sum('quantity'),
                faqat_tolangan=Sum('quantity', filter=Q(type_payment='paid'))
            )

            return Response({
                "today_sales_count": stats['faqat_tolangan'] or 0
            })

@extend_schema(tags=["statistic"])
class TodayRevenueView(APIView):
    def get(self, request, *args, **kwargs):
        today = timezone.now().date()
        today_sales = Stock.objects.filter(
            date__date=today,
            type="out"
        )

        total_revenue = today_sales.aggregate(
            total_sum=Sum(
                F('quantity') * F('medicine__price'),
                output_field=DecimalField()
            )
        )['total_sum'] or 0

        return Response({
           "bugungi_jami_tushum":total_revenue,

        })

@extend_schema(tags=["stock"])
class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockModelSerializer



@extend_schema(tags=["stock"])
class ExpiringCountMedicinesView(ListAPIView):
    queryset = Medicines.objects.filter(is_active=True).all()
    serializer_class = MedicModelSerializer
    def get_queryset(self):
        data  = Medicines.objects.filter(quantity__lt=70)
        return data

@extend_schema(tags=["statistic"])
class WeeklySalesStatView(APIView):
    def get(self, request):
        today = timezone.now().date()
        week_ago = today - timedelta(days=6)

        sales = Stock.objects.filter(
            date__date__gte=week_ago,
            type_payment='paid'
        ).values('date__date').annotate(
            total=Sum('medicine__price')
        ).order_by('date__date')

        days_map = {0: 'Du', 1: 'Se', 2: 'Ch', 3: 'Pa', 4: 'Ju', 5: 'Sh', 6: 'Ya'}

        result = []
        total_week = 0
        max_val = 0
        best_day = ""

        for i in range(7):
            current_day = week_ago + timedelta(days=i)
            day_sale = next((item['total'] for item in sales if item['date__date'] == current_day), 0)

            day_name = days_map[current_day.weekday()]
            result.append({"day": day_name, "amount": day_sale})

            total_week += day_sale
            if day_sale >= max_val:
                max_val = day_sale
                best_day = current_day.strftime('%A')

        return Response({
            "chart_data": result,
            "weekly_total": total_week,
            "best_day": best_day
        })

@extend_schema(tags=["statistic"])
class TopSellingMedicinesView(APIView):
    def get(self, request):
        top_medicines = Stock.objects.filter(type_payment='paid').values(
            'medicine__name'
        ).annotate(
            total_sold=Sum('quantity')
        ).order_by('-total_sold')[:5]

        return Response(top_medicines)


@extend_schema(tags=["supp"],summary="Yetkazib beruvchi qushish va uchirish")
class SupModelViewSet(ModelViewSet):
    queryset = Suppliers.objects.all()
    serializer_class = SupModelSerializer


@extend_schema(tags=["statistic"])
class MonthlySalesStatView(APIView):
    def get(self, request):
        today = timezone.now().date()
        start_of_month = today.replace(day=1)

        sales = Stock.objects.filter(
            date__date__range=[start_of_month, today],
            type_payment='paid'
        ).values('date__date').annotate(
            total=Sum('medicine__price')
        ).order_by('date__date')

        sales_dict = {item['date__date']: item['total'] for item in sales}

        result = []
        total_monthly = 0
        max_val = 0
        best_day = None

        days_count = (today - start_of_month).days + 1

        for i in range(days_count):
            current_day = start_of_month + timedelta(days=i)
            day_sale = sales_dict.get(current_day, 0)

            result.append({
                "day": current_day.strftime('%d-%b'),
                "amount": day_sale
            })

            total_monthly += day_sale
            if day_sale >= max_val:
                max_val = day_sale
                best_day = current_day.strftime('%Y-%m-%d')

        return Response({
            "chart_data": result,
            "monthly_total": total_monthly,
            "best_day": best_day,
            "days_in_report": days_count
        })