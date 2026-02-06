from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import Http404
from .models import Task
from .forms import TaskForm, RegisterForm
import logging

logger = logging.getLogger('django.security')


@login_required
def task_list(request):
    tasks = Task.objects.filter(owner=request.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})


@login_required
def add_task(request):
    form = TaskForm(request.POST or None)
    if form.is_valid():
        task = form.save(commit=False)
        task.owner = request.user
        task.save()

        logger.info(
            "TASK CREATED | user=%s | task_id=%s | ip=%s",
            request.user.username,
            task.id,
            request.META.get('REMOTE_ADDR', 'UNKNOWN')
        )

        return redirect('tasks')

    return render(request, 'tasks/add_task.html', {'form': form})


@login_required
def delete_task(request, task_id):
    """
    Secure delete with authorization + audit logging
    """
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        # Task gerçekten yok → info log
        logger.info(
            "DELETE ATTEMPT ON NON-EXISTENT TASK | user=%s | task_id=%s | ip=%s",
            request.user.username,
            task_id,
            request.META.get('REMOTE_ADDR', 'UNKNOWN')
        )
        raise Http404

    if task.owner != request.user:
        # 🔐 GERÇEK UNAUTHORIZED ACCESS
        logger.warning(
            "UNAUTHORIZED DELETE ATTEMPT | user=%s | task_id=%s | owner=%s | ip=%s",
            request.user.username,
            task_id,
            task.owner.username,
            request.META.get('REMOTE_ADDR', 'UNKNOWN')
        )
        raise Http404  # enumeration protection

    # ✅ Authorized delete
    logger.info(
        "TASK DELETED | user=%s | task_id=%s | ip=%s",
        request.user.username,
        task_id,
        request.META.get('REMOTE_ADDR', 'UNKNOWN')
    )

    task.delete()
    return redirect('tasks')


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()      # password burada HASHLENİR
            login(request, user)    # auto login

            logger.info(
                "USER REGISTERED | username=%s | ip=%s",
                user.username,
                request.META.get('REMOTE_ADDR', 'UNKNOWN')
            )

            return redirect('tasks')
        else:
            # 🔐 FAILED REGISTRATION (password ASLA yok)
            username = request.POST.get('username', 'UNKNOWN')
            errors = form.errors.as_json()

            logger.warning(
                "FAILED REGISTRATION ATTEMPT | username=%s | errors=%s | ip=%s",
                username,
                errors,
                request.META.get('REMOTE_ADDR', 'UNKNOWN')
            )
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})
