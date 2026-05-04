from django.urls import path
from rest_framework.routers import DefaultRouter

from authentication.views import UserParameters
from medicines.views import MedModelViewSet, ExpiringMedicinesView, ExpiredProductsCountView, TodaySalesSummaryView, \
      TodayRevenueView, StockViewSet, ExpiringCountMedicinesView, WeeklySalesStatView, TopSellingMedicinesView, \
      SupModelViewSet, MonthlySalesStatView, CustomListApiView, AIConsultantView

router = DefaultRouter()
urlpatterns = [
      path('/medicines/expiring-soon/', ExpiringMedicinesView.as_view(), name='expiring-soon'),
      path("/medicines/count/",ExpiredProductsCountView.as_view(),name="count medicines"),
      path("/medicines/sale/count/",TodaySalesSummaryView.as_view(),name="count  sale medicines"),
      path("/medicines/sale/sum/", TodayRevenueView.as_view(), name="sum sale medicines"),
      path("/medicines/count/less/",ExpiringCountMedicinesView.as_view(),name="count less medicines"),
      path('/stats/weekly-sales/', WeeklySalesStatView.as_view(), name='weekly-stats'),
      path('/stats/top-selling/', TopSellingMedicinesView.as_view(), name='top-selling'),
      path('/sale/month/',MonthlySalesStatView.as_view(),name="sale-month"),
      path('/list/custom/', CustomListApiView.as_view(), name="customs"),
      path('/ai-consultant/', AIConsultantView.as_view(), name='ai_consultant'),

]

router.register(r'/med', MedModelViewSet , basename='med')
router.register(r'/stock', StockViewSet , basename='stock')
router.register(r'/supp',SupModelViewSet,basename="supp")
router.register(r'/user/parameters', UserParameters , basename='user parameters')
urlpatterns += router.urls

