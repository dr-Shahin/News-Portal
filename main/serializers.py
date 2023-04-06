from rest_framework import serializers
from .models import Newsdata



# class NewsdataSerializers(serializers.ModelSerializer):
#     link= serializers.CharField(max_length=50)
#     basliq= serializers.CharField(max_length=100)
#     foto= serializers.CharField(max_length=1000)
#     metn= serializers.CharField(max_length=1000)
#     kateqoriya = serializers.CharField(max_length=25)
#     tarix= serializers.DateField(auto_now=True)

#     class Meta:
#         model = Newsdata
#         fields = ("__all__")