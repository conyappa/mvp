from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation
from django import forms
from .models import EmailListEntry


class EmailListEntryType(DjangoObjectType):
    class Meta:
        model = EmailListEntry
        fields = ("email",)


class EmailListEntryForm(forms.ModelForm):
    class Meta:
        model = EmailListEntry
        fields = ("email",)


class EmailEntryMutation(DjangoModelFormMutation):
    class Meta:
        form_class = EmailListEntryForm
