from rest_framework import serializers
from .models import ElectronicsNetwork
from .validators import validate_all

from rest_framework import serializers
from .models import ElectronicsNetwork
from .validators import validate_all


class ElectronicsNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectronicsNetwork
        fields = '__all__'
        read_only_fields = ('debt_to_supplier',)

    def validate(self, data):
        if self.instance:
            temp_instance = ElectronicsNetwork.objects.get(pk=self.instance.pk)
            for attr, value in data.items():
                setattr(temp_instance, attr, value)
        else:
            temp_instance = ElectronicsNetwork(**data)

        validate_all(temp_instance)
        return data