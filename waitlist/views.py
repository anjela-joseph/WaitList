from django.shortcuts import render, get_object_or_404
from .forms import WaitlistForm
from .models import WaitlistEntry
from django.core.mail import EmailMessage

def waitlist_view(request):
    message = None
    if request.method == 'POST':
        form = WaitlistForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            contact = form.cleaned_data['contact']
            email = form.cleaned_data['email']
            course = form.cleaned_data['course']

            entry, created = WaitlistEntry.objects.get_or_create(
                email=email,
                defaults={
                    'name': name,
                    'contact': contact,
                    'course': course,
                }
            )

            if created:
                # Send confirmation email (no QR)
                confirm_url = request.build_absolute_uri(f'/waitlist/confirm/{entry.token}/')
                body = f"Thanks for joining the waitlist!\nClick here to confirm: {confirm_url}"
                email_msg = EmailMessage(
                    'Waitlist Confirmation',
                    body,
                    to=[email]
                )
                email_msg.send()

                message = "You’ve been added to the waitlist. Check your email."
            else:
                # Already registered
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
