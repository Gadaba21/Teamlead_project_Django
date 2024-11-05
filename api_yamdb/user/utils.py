from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

from api_yamdb.settings import NOREPLAY_EMAIL


def generate_confirmation_code(user):
    """Генерация кода подтверждения с использованием Django токенов."""
    return default_token_generator.make_token(user)


def send_confirmation_email(email, confirmation_code):
    """Отправка email с кодом подтверждения."""
    send_mail(
        subject='Ваш код подтверждения',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email=NOREPLAY_EMAIL,
        recipient_list=(email,)
    )
