from django.shortcuts import render, get_object_or_404
from .forms import WaitlistForm
from .models import WaitlistEntry
from django.core.mail import EmailMessage
import qrcode
from io import BytesIO

def waitlist_view(request):
    message = None
    if request.method == 'POST':
        form = WaitlistForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            course = form.cleaned_data['course']
            entry, created = WaitlistEntry.objects.get_or_create(
                email=email, defaults={'course': course}
            )
            if form.is_valid():
                email = form.cleaned_data['email']
                entry, created = WaitlistEntry.objects.get_or_create(
                    email=email,
                    defaults={
            'name': form.cleaned_data['name'],
            'contact': form.cleaned_data['contact'],
            'course': form.cleaned_data['course'],
        }
    )

            if created:
                # Generate QR
                confirm_url = request.build_absolute_uri(f'/waitlist/confirm/{entry.token}/')
                qr = qrcode.make(confirm_url)
                buffer = BytesIO()
                qr.save(buffer)

                # Send email
                body = f"Thanks for joining the waitlist!\nClick or scan: {confirm_url}"
                email_msg = EmailMessage(
                    'Waitlist Confirmation',
                    body,
                    to=[email]
                )
                email_msg.attach('qr.png', buffer.getvalue(), 'image/png')
                email_msg.send()

                message = "You’ve been added to the waitlist. Check your email."
            else:
                body = f"Hi! You're already on the waitlist for the course: {entry.course}.\nNo need to register again."
                email_msg = EmailMessage(
                    'Waitlist Confirmation',
                    body,
                    to=[email]
                )
                email_msg.send()
                message = "You're already on the waitlist. We’ve sent you a confirmation email."


    else:
        form = WaitlistForm()
    return render(request, 'waitlist/waitlist_form.html', {'form': form, 'message': message})


def confirm_view(request, token):
    entry = get_object_or_404(WaitlistEntry, token=token)
    return render(request, 'waitlist/confirmation.html', {'entry': entry})
