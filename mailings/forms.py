from django import forms

from mailings.models import Mailing, Client, Message


class StyleMixin(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name != 'is_active':
                field.widget.attrs["class"] = "form-control"


class MailingForm(StyleMixin):

    class Meta:
        model = Mailing
        exclude = ("owner",)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        user = self.request.user
        super().__init__(*args, **kwargs)
        self.fields["clients"].queryset = Client.objects.filter(owner=user)
        self.fields["message"].queryset = Message.objects.filter(owner=user)


class MailingChangeStatusForm(StyleMixin):
    class Meta:
        model = Mailing
        fields = ("status",)


class MessageForm(StyleMixin):

    class Meta:
        model = Message
        fields = "__all__"


class ClientForm(StyleMixin):

    class Meta:
        model = Client
        fields = "__all__"
