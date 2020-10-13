from django.core.mail import send_mail
from django.views.generic import CreateView

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = "/auth/login/"
    template_name = "users/signup.html"

    def form_valid(self, form):
        email = form.cleaned_data['email']
        send_mail(
            'Регистрация',
            'Вы успешно прошли регистрацию на сайте Yatube.',
            'team.yatube@yandex.ru',
            [email],
            fail_silently=True,
        )
        return super().form_valid(form)
