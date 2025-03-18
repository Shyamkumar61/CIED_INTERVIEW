from django.urls import path
from .views import (
    MedicineList,
    MedicineDetail,
    BillingView,
    GetStockList,
    BillListView,
    UserReportView,
    CategoryListSerializer,
    CategoryDetailSerializer,
    SupplierListSerializer,
    MedicineSelectView,
)


app_name = "store"

urlpatterns = [
    path("medicines/", MedicineList.as_view(), name="medicine-list"),
    path("medicines/<int:pk>", MedicineDetail.as_view(), name="medicine-detail"),
    path("billing/", BillingView.as_view(), name="billing-list"),
    path("bills/", BillListView.as_view(), name="bill-list"),
    path("category/", CategoryListSerializer.as_view(), name="category-list"),
    path(
        "category/<int:pk>", CategoryDetailSerializer.as_view(), name="category-detail"
    ),
    path("supplier/", SupplierListSerializer.as_view(), name="supplier-list"),
    path("supplier/<int:pk>", SupplierListSerializer.as_view(), name="supplier-detail"),
    path("medicine-select/", MedicineSelectView.as_view(), name="medicine-select"),
    path("dashboard/stock-list/", GetStockList.as_view(), name="stock-list"),
    path("dashboard/report/", UserReportView.as_view(), name="user-report"),
]
