from django.shortcuts import render, redirect
from .forms import TextForm
import os
from django.conf import settings
from datetime import datetime

def index(request):
    log_file_path = os.path.join(settings.BASE_DIR, 'ex02', 'logs.txt')

    # Initialize history
    history = []
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as f:
            history = f.readlines()

    if request.method == 'POST':
        form = TextForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_entry = f"{timestamp} - {text}\n"

            # Append the new entry to the log file
            with open(log_file_path, 'a') as f:
                f.write(log_entry)

            # Redirect to avoid form resubmission on page refresh
            return redirect('index')
    else:
        form = TextForm()

    # Read the log file to display history
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as f:
            history = f.readlines()

    return render(request, 'ex02/index.html', {'form': form, 'history': history})