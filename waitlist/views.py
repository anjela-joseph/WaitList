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
                body = f"""
Hi {form.cleaned_data['name']},

You’re officially on the waiting list and we’re so glad to have you here!

We’re putting the final touches on the course, and as soon as it’s ready, you’ll be the first to know. No need to keep checking — we’ll drop into your inbox the moment enrollment opens.

Until then, if you have any questions or just want to say hi, we’re always happy to hear from you.

Excited to share more soon,  
Joseph Sudhip  
Declutter Minds
"""
                email_msg = EmailMessage(
                    "You're In! We'll Keep You Posted ",
                    body,
                    to=[email]
                )
                email_msg.send()

                message = "You’ve been added to the waitlist. Check your inbox for a confirmation!"
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
def confirm_view(request, token):
    entry = get_object_or_404(WaitlistEntry, token=token)
    return render(request, 'waitlist/confirmation.html', {'entry': entry})