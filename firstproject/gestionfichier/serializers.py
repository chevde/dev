from rest_framework import serializers
from .models import Annonce, UploadImage

class UploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadImage
        fields = ['id', 'image']

class AnnonceSerializer(serializers.ModelSerializer):
    images = UploadImageSerializer(many=True, required=False)

    class Meta:
        model = Annonce
        fields = ['id', 'user', 'title', 'description', 'images']

    def create(self, validated_data):
        images_data = self.context['request'].FILES.getlist('images')
        annonce = Annonce.objects.create(**validated_data)
        for image_data in images_data:
            UploadImage.objects.create(annonce=annonce, image=image_data)
        return annonce
