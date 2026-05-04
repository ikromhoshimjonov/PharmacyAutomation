from django.db.models import CASCADE, SET_NULL
from django.db.models import Model, CharField, ForeignKey, DecimalField, TextField, DateField, TextChoices, \
    IntegerField, DateTimeField , BooleanField

class Medicines(Model):
    name = CharField(max_length=255)
    price = DecimalField(max_digits=10,decimal_places=2)
    expiry_date =DateField()
    description = TextField(blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    quantity = IntegerField()
    grams = CharField(max_length=255)
    is_active = BooleanField(default=True)

    class StatusCategory(TextChoices):
        ALL = "all" , "All"
        YOUNG = "young", "Young"
        TEENAGERS = "teenagers", "Teenagers"
        ADULTS = "adults", "Adults"

    category = CharField(max_length=25, choices=StatusCategory)
    custom = ForeignKey("medicines.CustomerMedicine",on_delete=CASCADE)


    def __str__(self):
        return self.name

class Suppliers(Model):
    name = CharField(max_length=255)
    phone = CharField(max_length=13)
    address = TextField()

    def __str__(self):
        return self.name

class Stock(Model):
    class StatusMedication(TextChoices):
        IN = "in","In"
        OUT = "out","Out"

    class StatusPaymentMedication(TextChoices):
        PAID = "paid","Paid"
        PROCESS = "process","Process"
        REJECTED  = "rejected" , "Rejected"
    quantity = IntegerField()
    date = DateTimeField(auto_now_add=True)
    type = CharField(max_length=25,choices=StatusMedication)
    type_payment = CharField(max_length=25, choices=StatusPaymentMedication)

    medicine = ForeignKey("medicines.Medicines",on_delete=CASCADE)
    supplier = ForeignKey("medicines.Suppliers", on_delete=SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.medicine.name

class CustomerMedicine(Model):
    custom_name = CharField(max_length=255,null=True, blank=True)

    def __str__(self):
        return self.custom_name
