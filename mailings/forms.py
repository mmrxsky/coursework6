from django import forms

from mailings.models import Mailing, Client, Message


class StyleMixin(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            #if field_name != 'current_version_indicator' and field_name != 'publication_sign' and field_name != 'is_published':
            field.widget.attrs["class"] = "form-control"


class MailingForm(StyleMixin):

    class Meta:
        model = Mailing
        fields = '__all__'


class MessageForm(StyleMixin):

    class Meta:
        model = Message
        fields = '__all__'