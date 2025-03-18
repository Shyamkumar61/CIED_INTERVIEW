from rest_framework import serializers
from unicodedata import category

from apps.account.models import Account
from apps.store.models import Medicine, Bill, BillItem, Category, Supplier
from django.shortcuts import get_object_or_404


class CategoryListSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField(source="id", read_only=True)
    name = serializers.CharField(source="name")


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ("id", "name", "description")


class SupplierListSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField(source="id")
    name = serializers.CharField(source="name")


class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = ("id", "name", "description")


class MedicineSelectSerializer(serializers.Serializer):

    id = serializers.IntegerField(source="id")
    name = serializers.CharField(source="name")


class MedicineListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Medicine

    def __init__(self, *args, **kwargs):
        request = (
            kwargs["context"]["request"]
            if "context" in kwargs and "request" in kwargs["context"]
            else None
        )
        if request.method == "POST":
            self.Meta.fields = (
                "name",
                "description",
                "stock_quantity",
                "packaging_type",
                "expiry_date",
                "price",
                "supplier",
                "category",
            )
        else:
            self.Meta.fields = (
                "id",
                "name",
                "description",
                "packaging_type",
                "price",
                "expiry_date",
                "stock_quantity",
            )
        super().__init__(*args, **kwargs)


class MedicineStockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Medicine
        fields = ("id", "name", "stock_quantity", "expiry_date")


class UserReportSerializer(serializers.ModelSerializer):

    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_bills = serializers.IntegerField(read_only=True)

    class Meta:
        model = Account
        fields = ("id", "username", "email", "total_bills", "total_amount")


class MedicineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Medicine
        exclude = ("created", "modified")
        read_only_fields = ("", "created", "modified")

    def create(self, validated_data):
        category = get_object_or_404(Category, pk=validated_data.pop("category"))
        supplier = get_object_or_404(Supplier, pk=validated_data.pop("supplier"))
        medicine = Medicine.objects.create(category, supplier, **validated_data)
        return medicine

    def update(self, instance, validated_data):
        validated_data["stock_quantity"] = instance.stock_quantity + int(
            validated_data.get("stock_quantity")
        )
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        represent["supplier"] = instance.supplier.name
        represent["category"] = instance.category.name
        return represent


class BillItemListSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillItem
        exclude = ("created", "modified")

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["staff"] = instance.staff.get_full_name()
        response["medicine"] = instance.medicine.name
        return response


class BillItemSerializer(serializers.ModelSerializer):

    # Medicine is a List so that the Staff can add multiple Medicine in a single Bill
    medicine = serializers.IntegerField(write_only=True)

    class Meta:
        model = BillItem
        exclude = ("created", "modified", "price", "staff")

    def create(self, validated_data):
        staff = self.context["request"].user
        medicine = get_object_or_404(
            Medicine,
            id=validated_data["medicine"],
            packaging_type=validated_data["packaging_type"],
        )
        if not medicine:
            raise serializers.ValidationError(
                f"Invalid medicine or Packing Type Invalid"
            )
        if medicine.stock_quantity <= validated_data["quantity"]:
            raise serializers.ValidationError(
                f"Insufficient stock for {medicine.name} ({medicine.packaging_type}) Only {medicine.stock_quantity} stock can be purchased"
            )
        get_price = medicine.price * validated_data["quantity"]
        bill = BillItem.objects.create(
            staff=staff,
            price=get_price,
            medicine=medicine,
            quantity=validated_data["quantity"],
            packaging_type=validated_data["packaging_type"],
        )
        return bill
