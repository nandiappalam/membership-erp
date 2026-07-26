from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import EventForm
from django.http import JsonResponse
from django.db.models import Q




@login_required(login_url="login")
def event_list(request):

    events = Event.objects.all().order_by("-event_date", "-id")

    context = {
        "events": events,
    }

    return render(
        request,
        "events/event_list.html",
        context,
    )


@login_required(login_url="login")
def event_create(request):

    if request.method == "POST":

        form = EventForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Event Created Successfully."
            )

            return redirect("event_list")

    else:

        form = EventForm()

    context = {
        "form": form,
        "title": "Create Event",
    }

    return render(
        request,
        "events/event_form.html",
        context,
    )


@login_required(login_url="login")
def event_edit(request, id):

    event = get_object_or_404(
        Event,
        id=id
    )

    if request.method == "POST":

        form = EventForm(
            request.POST,
            instance=event
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Event Updated Successfully."
            )

            return redirect("event_list")

    else:

        form = EventForm(instance=event)

    context = {
        "form": form,
        "title": "Edit Event",
    }

    return render(
        request,
        "events/event_form.html",
        context,
    )


@login_required(login_url="login")
def event_delete(request, id):

    event = get_object_or_404(
        Event,
        id=id
    )

    if request.method == "POST":

        event.delete()

        messages.success(
            request,
            "Event Deleted Successfully."
        )

        return redirect("event_list")

    context = {
        "event": event,
    }

    return render(
        request,
        "events/event_delete.html",
        context,
    )

@login_required(login_url="login")
def attendance_list(request):

    attendances = EventAttendance.objects.select_related(
        "event",
        "member"
    )

    return render(
        request,
        "events/attendance_list.html",
        {
            "attendances": attendances,
        },
    )

@login_required(login_url="login")
def attendance_add(request):

    events = Event.objects.filter(status="OPEN")

    return render(
        request,
            "events/attendance_form.html",
        {
            "events": events,
        },
    )


@login_required(login_url="login")
def attendance_save(request):

    if request.method != "POST":
        return JsonResponse({
            "status": False,
            "message": "Invalid Request"
        })

    event = get_object_or_404(
        Event,
        id=request.POST.get("event")
    )

    member = get_object_or_404(
        Member,
        id=request.POST.get("member")
    )

    if EventAttendance.objects.filter(
        event=event,
        member=member
    ).exists():

        return JsonResponse({
            "status": False,
            "message": "Member already checked in."
        })

    attendance = EventAttendance.objects.create(
        event=event,
        member=member,
        entry_type="MEMBER",
        checkin_method="MANUAL"
    )

    coupon_no = ""

    coupon = None
    coupon_no = ""

    if event.gift_coupon:

        coupon = EventCoupon.objects.create(
            event=event,
            attendance=attendance
        )

        attendance.coupon_issued = True
        attendance.save()

        coupon_no = coupon.coupon_no

    return JsonResponse({
        "status": True,
        "message": "Check-in Successful",
        "coupon": coupon_no,
        "coupon_id": coupon.id if coupon else None,
    })



@login_required(login_url="login")
def search_member(request):

    search = request.GET.get("search", "").strip()
    event_id = request.GET.get("event")

    if not search:
        return JsonResponse({
            "status": False,
            "message": "Enter Membership No or Mobile Number"
        })

    member = Member.objects.filter(
        models.Q(membership_no__iexact=search) |
        models.Q(mobile__iexact=search)
    ).first()

    if not member:
        return JsonResponse({
            "status": False,
            "message": "Member not found"
        })

    attended = False

    if event_id:
        attended = EventAttendance.objects.filter(
            event_id=event_id,
            member=member
        ).exists()

    return JsonResponse({

        "status": True,

        "id": member.id,

        "membership_no": member.membership_no,

        "name": member.owner_name,

        "mobile": member.mobile,

        "company": member.company_name,

        "valid_upto": str(member.membership_valid_upto),

        "photo": member.photo.url if member.photo else "",

        "attended": attended,
    })


@login_required(login_url="login")
def coupon_print(request, id):

    coupon = get_object_or_404(
        EventCoupon.objects.select_related(
            "attendance__member",
            "event",
        ),
        id=id,
    )

    return render(
        request,
        "events/coupon_print.html",
        {
            "coupon": coupon,
        },
    )

def print_coupon(request, id):

    registration = get_object_or_404(
        EventRegistration,
        id=id
    )

    return render(
        request,
        "events/coupon_print.html",
        {
            "registration": registration
        }
    )

