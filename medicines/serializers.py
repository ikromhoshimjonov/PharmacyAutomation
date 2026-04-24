from requests import Response
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers, status
from medicines.models import Medicines, Stock, Suppliers, CustomerMedicine


class MedModelSerializer(ModelSerializer):
    class Meta:
        model=Medicines
        fields = "__all__"
        # fields = "id","name","price","expiry_date","description","category","grams","quantity","custom"




class CustomerModelSerializer(ModelSerializer):
    class Meta:
        model = CustomerMedicine
        fields ="id", "custom_name",


class StockModelSerializer(ModelSerializer):
    supplier = serializers.PrimaryKeyRelatedField(
        queryset=Suppliers.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Stock
        fields = ["id", "medicine", "supplier", "quantity", "type", "type_payment", "date"]

    def to_representation(self, instance):
        res = super().to_representation(instance)
        if instance.medicine:
            res['medicine_name'] = instance.medicine.name
            res['medicine_category'] = instance.medicine.category
            res['medicine_price'] = instance.medicine.price
            res['medicine_grams'] = getattr(instance.medicine, 'grams', '')
        return res

    def validate(self, data):
        medicine = data.get('medicine')
        quantity = data.get('quantity')
        stock_type = data.get('type', 'out')


        if stock_type == 'out':
            if medicine.quantity < quantity:
                raise serializers.ValidationError({
                    "quantity": f"Omborda yetarli emas. Mavjud: {medicine.quantity}"
                })
        return data

    def create(self, validated_data):
        medicine = validated_data['medicine']
        quantity = validated_data['quantity']
        stock_type = validated_data.get('type', 'out')


        stock_instance = Stock.objects.create(**validated_data)

        if stock_type == 'out':
            medicine.quantity -= quantity
        else:
            medicine.quantity += quantity


        if medicine.quantity <= 0:
            medicine.quantity = 0
            medicine.is_active = False
        else:
            medicine.is_active = True

        medicine.save()

        return stock_instance


class MedicModelSerializer(ModelSerializer):
    class Meta:
        model=Medicines
        fields = "name","quantity"


class WeeklySalesSerializer(serializers.Serializer):
    day = serializers.CharField()
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2)


class SupModelSerializer(ModelSerializer):
    class Meta:
        model=Suppliers
        fields = "name","phone","address"


