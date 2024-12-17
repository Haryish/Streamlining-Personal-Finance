from rest_framework import serializers
from .models import *

from rest_framework import serializers
from .models import Addmoney_info

class AddmoneyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addmoney_info
        fields = ['user', 'add_money', 'quantity', 'Date', 'Category']
