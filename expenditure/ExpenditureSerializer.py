from rest_framework import serializers
from .models import Expenditure


# category
class ExpenditureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenditure
        fields = "__all__"
