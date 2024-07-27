from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from django.utils import timezone
from django.conf import settings

import os
import sys
import datetime

from .models import Barcodes, Feedback, Photo
from .forms import PhotoForm, FeedbackForm, RegisterForm

sys.path.insert(1, 'D:\Личное\Програмирование\Django projects\ProductSite\Project\media\photos')
import script


def index(request):
    """View function for home page of site."""

    num_barcodes = Barcodes.objects.all().count()
    num_feedbacks = Feedback.objects.all().count()

    # num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    context = {
        'num_barcodes': num_barcodes,
        'num_feedbacks': num_feedbacks,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'registration/signup.html', {'form': form})
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'registration/signup.html', {'form': form})


def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save()
            photo = get_object_or_404(Photo, pk=photo.id)
            barcode = script.run_decoding(photo.image)
            if not barcode:
                return HttpResponseNotFound("<h1>На фотографии не найдено штрих-кодов</h1>")
            os.remove(f'D:\Личное\Програмирование\Django projects\ProductSite\Project\media\{photo.image}')
            Photo.objects.filter(pk=photo.id).delete()
            return HttpResponseRedirect(reverse('barcode_detail', args=[barcode]))
    else:
        form = PhotoForm()
    return render(request, 'scaner.html', {'form': form})


@login_required
def barcode_detail(request, barcode):
    login_url = '/signup/'
    redirect_field_name = 'barcode_detail'
    try:
        detail_code = Barcodes.objects.get(barcode=barcode)
        my_feedback = Feedback.objects.filter(id_author=request.user, id_barcode=detail_code)
        if my_feedback:
            my_feedback = my_feedback[0]
        feedbacks = Feedback.objects.filter(id_barcode=detail_code).exclude(id_author=request.user)
    except ObjectDoesNotExist:
        detail_code = None
        bar = Barcodes(barcode=barcode)
        bar.save()
    if request.method == 'POST' and not my_feedback:
        form = FeedbackForm(request.POST)
        if form.is_valid() and request.user.id:
            feed = form.save(commit=False)
            feed.id_barcode = detail_code
            feed.id_author = request.user
            feed.time_creation = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            feed.save()
            return render(request, 'barcode_detail.html', {'barcode': barcode,
                                                           'detail_code': detail_code,
                                                           'my_feedback': my_feedback,
                                                           'feedbacks': feedbacks})
        elif not request.user.id:
            return HttpResponseRedirect(reverse('signup'))
    elif my_feedback:
        return render(request, 'barcode_detail.html', {'barcode': barcode,
                                                       'detail_code': detail_code,
                                                       'my_feedback': my_feedback,
                                                       'feedbacks': feedbacks})
    else:
        form = FeedbackForm()
    return render(request, 'barcode_detail_form.html', {'barcode': barcode,
                                                        'detail_code': detail_code,
                                                        'form': form,
                                                        'my_feedback': my_feedback,
                                                        'feedbacks': feedbacks})

