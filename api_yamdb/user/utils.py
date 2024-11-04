import hashlib

from django.core.mail import send_mail

from api.constants import CONFIRM_CODE_LEN


def generate_confirmation_code(user):
    data = f'{user.username}{user.email}'
    return hashlib.sha256(data.encode()).hexdigest()[:CONFIRM_CODE_LEN]


def send_confirmation_email(email, confirmation_code):
    """Отправка email с кодом подтверждения."""
    send_mail(
        subject='Ваш код подтверждения',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email='noreply@example.com',
        recipient_list=[email]
    )
