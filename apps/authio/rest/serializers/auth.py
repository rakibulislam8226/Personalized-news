from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework import serializers

from ...utils import default_countries, default_keywords, default_sources

User = get_user_model()


class UserRegistrationListSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """

    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "confirm_password",
            "first_name",
            "last_name",
            "countries",
            "sources",
            "keywords",
        )

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Password and Confirm Password do not match."}
            )
        try:
            validate_password(data["password"])
        except DjangoValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return data

    def create(self, validated_data):
        countries = validated_data.get("countries") or default_countries()
        sources = validated_data.get("sources") or default_sources()
        keywords = validated_data.get("keywords") or default_keywords()
        user = User(
            email=validated_data["email"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            countries=countries,
            sources=sources,
            keywords=keywords,
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "countries",
            "sources",
            "keywords",
        )
        read_only_fields = ("email",)
        extra_kwargs = {
            "countries": {"default": default_countries()},
            "sources": {"default": default_sources()},
            "keywords": {"default": default_keywords()},
        }

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.countries = validated_data.get("countries", instance.countries)
        instance.sources = validated_data.get("sources", instance.sources)
        instance.keywords = validated_data.get("keywords", instance.keywords)
        instance.save()
        return instance
