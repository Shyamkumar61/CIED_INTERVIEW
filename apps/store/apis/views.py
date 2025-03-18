from rest_framework import generics
from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.db.models import Sum, Count, Q
from apps.store.apis.serializers import (
    MedicineSerializer,
    MedicineListSerializer,
    MedicineStockSerializer,
    BillItemSerializer,
    BillItemListSerializer,
    UserReportSerializer,
    CategoryListSerializer,
    SupplierListSerializer,
    SupplierSerializer,
    CategorySerializer,
)
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.store.models import Medicine, BillItem, Category, Supplier
from rest_framework.exceptions import ValidationError
from apps.store.permissions import MangerPermission, StaffPermission
from apps.account.permissions import AccountPermissions
from rest_framework import status


User = get_user_model()


class CategoryListSerializer(generics.ListCreateAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, MangerPermission)
    queryset = Category.objects.only("id", "name")
    serializer_class = CategoryListSerializer


class CategoryDetailSerializer(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, MangerPermission)
    serializer_class = CategorySerializer

    def get_object(self):
        return get_object_or_404(Category, id=self.kwargs["pk"])


class SupplierListSerializer(generics.ListCreateAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, MangerPermission)
    queryset = Supplier.objects.only("id", "name")
    serializer_class = SupplierListSerializer


class SupplierDetailSerializer(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, MangerPermission)
    serializer_class = SupplierSerializer

    def get_object(self):
        return get_object_or_404(Supplier, id=self.kwargs["pk"])


class MedicineSelectView(generics.ListCreateAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, MangerPermission)
    serializer_class = MedicineSerializer
    queryset = Medicine.objects.only("id", "name")


class MedicineList(generics.ListCreateAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, MangerPermission)
    queryset = Medicine.objects.all()
    serializer_class = MedicineListSerializer


class MedicineDetail(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, MangerPermission)
    serializer_class = MedicineSerializer

    def get_object(self):
        queryset = get_object_or_404(Medicine, pk=self.kwargs["pk"])
        return queryset


class BillingView(generics.CreateAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, StaffPermission)

    serializer_class = BillItemSerializer

    def get_queryset(self):
        return BillItem.objects.none()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetStockList(generics.ListAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, AccountPermissions)
    serializer_class = MedicineStockSerializer

    def get_queryset(self):
        queryset = Medicine.objects.only(
            "id",
            "name",
            "stock_quantity",
            "expiry_date",
        )
        return queryset


class BillListView(generics.ListAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, AccountPermissions)
    serializer_class = BillItemListSerializer

    def get_queryset(self):
        queryset = BillItem.objects.all()
        return queryset


class UserReportView(generics.ListAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, AccountPermissions)
    serializer_class = UserReportSerializer

    def get_queryset(self):
        queryset = User.objects.annotate(
            total_amount=Sum("staff__price", default=0),
            total_bills=Count("staff", distinct=True),
        )

        start_date = self.request.query_params.get("start_date")
        end_date = (
            self.request.query_params.get("end_date")
            if self.request.query_params.get("end_date")
            else datetime.now().date()
        )

        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, "%d-%m-%Y").date()
                end_date = (
                    datetime.strptime(end_date, "%d-%m-%Y").date()
                    if isinstance(end_date, str)
                    else datetime.now().date()
                )

                queryset = User.objects.annotate(
                    total_amount=Sum(
                        "staff__price",
                        filter=(
                            Q(staff__created__date__range=(start_date, end_date))
                            if start_date and end_date
                            else Q()
                        ),
                    ),
                    total_bills=Count(
                        "staff",
                        filter=(
                            Q(staff__created__date__range=(start_date, end_date))
                            if start_date and end_date
                            else Q()
                        ),
                    ),
                )
            except ValueError:
                raise ValidationError("Invalid date format. Use YYYY-MM-DD.")

        return queryset
