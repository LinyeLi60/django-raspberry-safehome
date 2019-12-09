# coding=utf-8
from django.shortcuts import HttpResponse, render
from django.http import StreamingHttpResponse
from safehome.forms import ControlPanelForm
from .models import UserExtension

from django.views.decorators.gzip import gzip_page
from .camera import VideoCamera
from safehome.forms import LoginForm

cam = VideoCamera()


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the safe index.")


# 设置参数
def configure(request):
    if request.method == "POST":
        control_panel_form = ControlPanelForm(request.POST)
        print(control_panel_form)
        if control_panel_form.is_valid():
            print("表单校验成功", control_panel_form)
            phone_number = control_panel_form.cleaned_data['phone_number']
            delay = control_panel_form.cleaned_data['delay']
            status = control_panel_form.cleaned_data['status']

            message = "Configuration update successful"
            username = request.session['username']

            user_extension = UserExtension.objects.get(user__username=username)
            user_extension.telephone_number = phone_number
            user_extension.dialing_delay = delay
            user_extension.is_stay = True if status == 'Stay' else False
            user_extension.save()
            print(user_extension)
        else:
            print("表单校验失败")
            message = "Please check the input as prompted"
        return render(request, 'safe/configure.html', locals())
    else:
        message = 'Configure'
        username = request.session['username']
        user_extension = UserExtension.objects.get(user__username=username)
        control_panel_form = ControlPanelForm(initial={'status': 'Stay' if user_extension.is_stay else 'Away',
                                                       'phone_number': user_extension.telephone_number,
                                                       'delay': user_extension.dialing_delay})

    return render(request, 'safe/configure.html', locals())


def gen(camera):
    while True:
        frame = cam.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip_page
def camera(request):
    if 'is_login' in request.session and request.session['is_login']:
        try:
            return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
        except Exception as e:    # This is bad! replace it with proper handling
            print("相机画面获取错误:", e)
    else:
        login_form = LoginForm()
        message = 'Please login first!'
        return render(request, 'login.html', locals())
