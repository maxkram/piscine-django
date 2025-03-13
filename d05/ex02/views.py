from django.shortcuts import render
from django.conf import settings
from .forms import TextForm
from datetime import datetime

def index(request):
    history = []
    if request.method == 'POST':
        form = TextForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_entry = f"{timestamp}: {text}\n"

            # Append the log entry to the log file
            with open(settings.LOG_FILE_PATH, 'a') as log_file:
                log_file.write(log_entry)

            # Reset the form after processing
            form = TextForm()
    else:
        form = TextForm()

    # Read the log file to display history
    try:
        with open(settings.LOG_FILE_PATH, 'r') as log_file:
            history = log_file.readlines()
    except FileNotFoundError:
        pass

    return render(request, 'ex02/index.html', {'form': form, 'history': history})