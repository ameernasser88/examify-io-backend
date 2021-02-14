from allauth.account.adapter import DefaultAccountAdapter
from.models import *
class CustomUserAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        from allauth.account.utils import user_field

        user = super().save_user(request, user, form, False)
        user_field(user, 'user_type', request.data.get('user_type', ''))
        user.save()
        return user