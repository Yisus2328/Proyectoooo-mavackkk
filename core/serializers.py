from rest_framework import serializers
from .models import *

#lo utilizamos para transformar python a json

class TipoArteSerializers(serializers.ModelSerializer):
        class Meta:
            model = TipoArte
            fields = '__all__'

class ArteSerializers(serializers.ModelSerializer):
        tipo_arte = TipoArteSerializers(read_only=True)

        class Meta:
            model = Arte
            fields = '__all__'