from django.contrib.auth import authenticate
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.password_validation import validate_password
from .models import UserAccount
from .utils import validate_email as email_valid


class RegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128,
        write_only=True,
        required=True,
        validators=[validate_password],
        # *to avoid explicit password
        style={"input_type": "password"},
    )

    # No validation for second pass, we will check passwords are the same
    password2 = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})

    class Meta:
        model = UserAccount
        fields = (
            "email",
            "name",
            "password",
            "password2",
        )
        # * arbitrary additional keyword arguments
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True},
        }

    def validate_email(self, value: str):
        """Normalize email and validate"""
        valid, error_text = email_valid(value)
        # if not true
        if not valid:
            raise serializers.ValidationError(error_text)

        try:
            email_name, domain_part = value.strip().rsplit("@", 1)
        except ValueError:
            pass
        else:
            value = "@".join([email_name, domain_part.lower()])

        return value

    def create(self, validated_data):
        """Return user after creation"""
        password = validated_data.get("password")
        validated_data.pop("password2")
        user = UserAccount.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    # * serializers validations => object level || field level
    def validate(self, data):

        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords must match")

        return data


class LoginSerializer(serializers.ModelSerializer):

    email = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
    password = serializers.CharField(
        max_length=255,
        style={"input_type": "password"},
    )

    # Read only field of token
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        """Get user token"""
        user = UserAccount.objects.get(email=obj.email)

        return {"refresh": user.tokens["refresh"], "access": user.tokens["access"]}

    class Meta:
        model = UserAccount
        fields = (
            "email",
            "name",
            "password",
            "tokens",
        )

    def validate(self, data):
        """validate and return user login"""
        email = data.get("email", None)
        password = data.get("password", None)

        if email is None:
            raise serializers.ValidationError("Email is required to login")

        if password is None:
            raise serializers.ValidationError("A password is required to login")

        # from abstractbaseuser
        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError("User not found")

        if not user.is_active:
            raise serializers.ValidationError("This user is not currently activaed")

        return user


class UserAccountSerializer(serializers.ModelSerializer):
    """Handle serialization and deserialization of user objects"""

    # update funct to update instance

    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = UserAccount
        fields = (
            "id",
            "email",
            "name",
            "password",
            # "tokens",
        )

        read_only_fields = ("tokens",)

    def update(self, instance, validated_data):
        """Perform an update on a user"""
        password = validated_data.pop("password", None)
        print(type(validated_data))

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance


class LogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField()

    def validate(self, attrs):
        """validate token"""
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        """validate save blacklisted token"""

        # blacklist upon logout
        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            raise exceptions.AuthenticationFailed(TokenError)
