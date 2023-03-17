from dataclasses import dataclass

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from users.models import User
from api_yamdb.settings import EMAIL_ROBOT


@dataclass
class ConfirmationManager():
    """Delivers the confirmation code."""

    user: User

    def get_message(self) -> str:
        """Generates a code message."""

        return f'''
        Имя пользователя: {self.user.username}
        confirmation_code: {default_token_generator.make_token(self.user)}
        '''

    def send_by_email(self) -> int:
        """Sends confirmation code by email."""

        subject = 'Код подтверждения регистрации в api_yamdb'

        return send_mail(
            subject,
            self.get_message(),
            EMAIL_ROBOT,
            [self.user.email],
            fail_silently=False
        )
