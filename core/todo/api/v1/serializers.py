from rest_framework import serializers
from todo.models import Task
from accounts.models import Profile


class TaskSerializer(serializers.ModelSerializer):
    relative_url = serializers.URLField(source='get_absolute_api_url', read_only=True)
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'author', 'title', 'complete', 'relative_url', 'absolute_url', 'created_date', 'updated_date']
        read_only = ['author']

    def get_absolute_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj)
    
    def to_representation(self, instance):
        # for get request object that send by user request
        request = self.context.get('request')
        rep = super().to_representation(instance)
        return rep
    
    def create(self, validated_data):
        validated_data['author'] = Profile.objects.get(user__id= self.context.get('request').user.id)
        return super().create(validated_data)