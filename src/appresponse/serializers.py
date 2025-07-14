from rest_framework import serializers


class StartSessionSerializer(serializers.Serializer):
    prompt = serializers.CharField(max_length=1000, required=True)


class ModifySongSerializer(serializers.Serializer):
    session_id = serializers.CharField(max_length=100, required=True)
    modification = serializers.CharField(max_length=1000, required=True)


class FinalizePlaylistSerializer(serializers.Serializer):
    session_id = serializers.CharField(max_length=100, required=True)


class SendMessageSerializer(serializers.Serializer):
    session_id = serializers.CharField(max_length=100, required=True)
    message = serializers.CharField(max_length=1000, required=True)


class DeleteSessionSerializer(serializers.Serializer):
    session_id = serializers.CharField(max_length=100, required=True)
