from django.contrib import admin
from django.db import models
from django.template import loader
from django.utils.translation import ugettext_lazy as _
from inscription.models import message_history
from inscription.utils import post_officer

NOT_CONFIRMED = 'NOT_CONFIRMED'
CONFIRMED = 'CONFIRMED'
WAITING_LIST = 'WAITING_LIST'
CANCELED = 'CANCELED'

TOTAL_PLACES = 230

STATUS_CHOICES = (
        (NOT_CONFIRMED, _('Not Confirmed')),
        (CONFIRMED, _('Confirmed')),
        (WAITING_LIST, _('Waiting List')),
        (CANCELED, _('Canceled')))


class InscriptionAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'status', 'address', 'email', 'phone', 'number_places', 'desired_place',
                    'registered')
    list_filter = ('status',)
    fieldsets = ((None, {'fields': ('last_name', 'first_name', 'status', 'address', 'email', 'phone', 'number_places',
                                    'desired_place')}),)
    search_fields = ['first_name', 'last_name', 'address', 'email', 'phone']


class Inscription(models.Model):
    first_name = models.CharField(max_length=30, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=30, verbose_name=_("Last Name"))
    address = models.TextField(verbose_name=_("Address"))
    email = models.EmailField(verbose_name=_("Email"), blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name=_("Phone"))
    number_places = models.IntegerField(verbose_name=_("Places"))
    desired_place = models.TextField(verbose_name=_("Desired Place"), blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NOT_CONFIRMED, verbose_name=_("Status"))
    registered = models.DateTimeField(null=True, auto_now=True, verbose_name=_("Registered"))

    def save(self, *args, **kwargs):
        send_email_when_registering(self)
        super(Inscription, self).save(*args, **kwargs)
        send_email_when_confirmed(self)

    def __str__(self):
        return "{}, {} - {}".format(self.last_name, self.first_name, self.number_places)


def send_email_when_registering(inscription):
    if not inscription.pk:
        if is_total_places_reached(getattr(inscription, 'number_places')):
            inscription.status = WAITING_LIST
            subject = _('Enrollment submission in waiting list')
            template = loader.get_template('messages/waiting_list_fr.eml')
            recipients = [inscription.email]
            post_officer.send_message(recipients, subject, template.render(), message_history.WAITING_LIST)
        else:
            subject = _('Enrollment Submission Confirmed')
            template = loader.get_template('messages/submission_confirmation_fr.eml')
            context = {'user': "{} {}".format(inscription.first_name, inscription.last_name)}
            recipients = [inscription.email]
            post_officer.send_message(recipients, subject, template.render(context),
                                      message_history.SUBMISSION_CONFIRMATION)


def send_email_when_confirmed(inscription):
    messages = message_history.find_messages(inscription.email, type=message_history.INSCRIPTION_CONFIRMATION).count()
    if inscription.email and inscription.status == CONFIRMED and messages == 0:
        subject = _('Enrollment Confirmed')
        template = loader.get_template('messages/confirmation_fr.eml')
        context = {'user': "{} {}".format(inscription.first_name, inscription.last_name),
                   'places': _("1 slot") if inscription.number_places == 1 else _("2 slots")}
        recipients = [inscription.email]
        post_officer.send_message(recipients, subject, template.render(context), message_history.INSCRIPTION_CONFIRMATION)


def find_confirmed_inscriptions():
    return Inscription.objects.filter(status=CONFIRMED).order_by('last_name')


def get_total_confirmed_places():
    sum_number_places = Inscription.objects.filter(status=CONFIRMED).aggregate(models.Sum('number_places'))
    if sum_number_places['number_places__sum']:
        return sum_number_places['number_places__sum']
    else:
        return 0


def get_total_demanded_places():
    sum_number_places = Inscription.objects.exclude(status=CANCELED).exclude(status=WAITING_LIST)\
                                   .aggregate(models.Sum('number_places'))
    if sum_number_places['number_places__sum']:
        return sum_number_places['number_places__sum']
    else:
        return 0


def get_notification_types(inscription):
    messages = message_history.find_messages(inscription.email)
    return [msg.type for msg in messages]


def is_total_places_reached(current_demand=0):
    existing_demand = get_total_demanded_places()
    return (existing_demand + current_demand) >= TOTAL_PLACES
