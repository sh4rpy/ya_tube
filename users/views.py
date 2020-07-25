from django.core.mail import send_mail
from django.views.generic import CreateView

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = "/auth/login/"
    template_name = "users/signup.html"

    def form_valid(self, form):
        email = form.cleaned_data['email']
        send_mail_to_right_address(email)
        return super().form_valid(form)


def send_mail_to_right_address(email):
    send_mail(
        'Регистрация', 'Вы успешно прошли регистрацию на сайте',
        'from@example.net', [email],
        fail_silently=False,
    )
