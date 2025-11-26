from datetime import date
import json
import time
from django.shortcuts import render
from django.views.generic import TemplateView, FormView, CreateView, ListView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import EmailMessage
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import loader
from django.http import HttpResponse, Http404, JsonResponse
from django.middleware.csrf import get_token
from .forms import ContactForm, SchedulePostForm, CalendarForm
from .models import SchedulePost, CustomUser

class IndexView(LoginRequiredMixin, ListView):
    template_name = 'schedule/index.html'
    model = SchedulePost
    paginate_by = 10

    def get_queryset(self):
        current_user = self.request.user.username
        user_data = CustomUser.objects.get(username = current_user)
        if user_data:
            queryset = SchedulePost.objects.filter(user = user_data, end_date__gte = date.today())
            queryset = queryset.order_by('end_date', 'start_date', '-posted_at')
        return queryset

class ContactView(FormView):
    template_name = 'schedule/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('schedule:contact')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        title = form.cleaned_data['title']
        message = form.cleaned_data['message']

        subject = 'お問い合せ： {}'.format(title)
        message = '送信者名： {0}\nメールアドレス： {1}\nタイトル： {2}\nメッセージ：\n{3}'.format(name, email, title, message)

        from_email = 'kmm2559381@stu.o-hara.ac.jp'
        to_list = ['kmm2559381@stu.o-hara.ac.jp']

        message = EmailMessage(
            subject = subject,
            body = message,
            from_email = from_email,
            to = to_list,
            )

        message.send()
        messages.success(self.request, 'お問い合わせは正常に送信されました')

        return super().form_valid(form)

class CreateScheduleView(LoginRequiredMixin, CreateView):
    form_class = SchedulePostForm
    template_name = 'schedule/post_schedule.html'
    success_url = reverse_lazy('schedule:index')

    def form_valid(self, form):
        postdata = form.save(commit = False)
        postdata.user = self.request.user
        postdata.save()

        messages.success(self.request, 'スケジュールの追加が完了しました')
        return super().form_valid(form)

class DeleteSuccessView(TemplateView):
    template_name = 'schedule/delete_success.html'

class ScheduleDetailView(LoginRequiredMixin ,DetailView):
    template_name = 'schedule/detail.html'
    model = SchedulePost

class CategoryView(LoginRequiredMixin, ListView):
    template_name = 'schedule/index.html'
    model = SchedulePost
    paginate_by = 10

    def get_queryset(self):
        current_user = self.request.user.username
        user_data = CustomUser.objects.get(username = current_user)
        category_id = self.kwargs['category']
        if user_data:
            queryset = SchedulePost.objects.filter(user = user_data, end_date__gte = date.today(), category = category_id)
            queryset = queryset.order_by('end_date', 'start_date', '-posted_at')
        return queryset

class ScheduleDeleteView(DeleteView):
    model = SchedulePost
    template_name = 'schedule/schedule_delete.html'
    success_url = reverse_lazy('schedule:delete_done')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'スケジュールの削除が完了しました')
        return super().delete(request, *args, **kwargs)

class ScheduleUpdateView(UpdateView):
    model = SchedulePost
    form_class = SchedulePostForm
    template_name = 'schedule/schedule_update.html'

    def get_success_url(self):
        return reverse_lazy('schedule:schedule_update', kwargs = {'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'スケジュールの更新が完了しました')
        return super().form_valid(form)

def calendar_view(request):
    get_token(request)
    template = loader.get_template('schedule/schedule_calendar.html')
    return HttpResponse(template.render())

def get_events(request):
    """
    イベントの取得
    """

    if request.method == "GET":
        # GETは対応しない
        raise Http404()

    # JSONの解析
    datas = json.loads(request.body)

    # バリデーション
    calendarForm = CalendarForm(datas)
    if calendarForm.is_valid() == False:
        # バリデーションエラー
        raise Http404()

    # リクエストの取得
    start_date = datas["start_date"]
    end_date = datas["end_date"]

    # 日付に変換。JavaScriptのタイムスタンプはミリ秒なので秒に変換
    formatted_start_date = time.strftime(
        "%Y-%m-%d", time.localtime(start_date / 1000))
    formatted_end_date = time.strftime(
        "%Y-%m-%d", time.localtime(end_date / 1000))

    # FullCalendarの表示範囲のみ表示
    events = SchedulePost.objects.filter(
        start_date__lt=formatted_end_date, end_date__gt=formatted_start_date, user = request.user
    )

    # fullcalendarのため配列で返却
    list = []
    for event in events:
        list.append(
            {
                "title": event.title,
                "start": event.start_date,
                "end": event.end_date,
            }
        )

    return JsonResponse(list, safe=False)