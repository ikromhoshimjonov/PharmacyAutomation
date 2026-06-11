import os

import numpy as np
from django.db.models import CASCADE, SET_NULL
from django.db.models import Model, CharField, ForeignKey, DecimalField, TextField, DateField, TextChoices, \
    IntegerField, DateTimeField , BooleanField ,BinaryField

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
SECRET_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=SECRET_KEY)


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
    embedding =BinaryField(null=True, blank=True, editable=False)

    class StatusCategory(TextChoices):
        ALL = "all" , "All"
        YOUNG = "young", "Young"
        TEENAGERS = "teenagers", "Teenagers"
        ADULTS = "adults", "Adults"

    category = CharField(max_length=25, choices=StatusCategory)
    custom = ForeignKey("medicines.CustomerMedicine",on_delete=CASCADE)

    def save(self, *args, **kwargs):
        # Tavsif o'zgarganda yoki yangi dori qo'shilganda embedding yaratish
        if self.description and not self.embedding:
            try:
                text = f"{self.name}. {self.description}"
                response = client.embeddings.create(
                    input=text,
                    model="text-embedding-3-small"
                )
                vector = response.data[0].embedding
                # Vektorni float32 formatida baytlarga o'giramiz
                self.embedding = np.array(vector, dtype=np.float32).tobytes()
            except Exception as e:
                print(f"Embedding yaratishda xato: {e}")

        super().save(*args, **kwargs)

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
