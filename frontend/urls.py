from django.urls import path
from frontend.views import index, register, login, figma, sale, product, product_table, expiry_medicine_table, \
    settings_table, report_table, product_in_out, product_question, similarity_question
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", index, name="frontend_index"),
    path("register/front/", register, name="frontend_register"),
    path("login/",login,name="frontend_login"),
    path('new/sale/',sale,name="new-sale"),
    path("new/product/",product , name="new-product"),
    path("product/table/",product_table,name="product-table"),
    path("expiry/medicine/",expiry_medicine_table,name="product-expiry"),
    path("settings/table/",settings_table,name="settings-table"),
    path("report/pharma/",report_table,name="report-pharma"),
    path("in/out/",product_in_out,name="in-out"),
    path("product/question/",product_question,name="question-pr"),
    path("similarity/pharma/",similarity_question,name="similarity")
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

