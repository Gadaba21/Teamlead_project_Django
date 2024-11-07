from django.core.mail import send_mail

from api_yamdb.settings import NOREPLAY_EMAIL


def send_confirmation_email(email, confirmation_code):
    """Отправка email с кодом подтверждения."""
    send_mail(
        subject='Ваш код подтверждения',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email=NOREPLAY_EMAIL,
        recipient_list=(email,)
    )
