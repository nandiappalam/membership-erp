from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import EventForm
from django.http import JsonResponse
from django.db.models import Q
from membership.models import *
from django.utils import timezone
import qrcode
import base64
from io import BytesIO
from django.conf import settings
from events.models import *



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

    # Mark as printed only the first time
    if not coupon.printed:
        coupon.printed = True
        coupon.printed_at = timezone.now()
        coupon.save(update_fields=["printed", "printed_at"])

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


def agm_entry(request, event_id):

    event = get_object_or_404(
        Event,
        id=event_id
    )


    if request.method == "POST":

        search_no = request.POST.get(
            "search_no"
        ).strip()


        # Search Member
        member = Member.objects.filter(
            Q(membership_no=search_no) |
            Q(mobile=search_no)
        ).first()


        if member:

            attendance, created = EventAttendance.objects.get_or_create(
                event=event,
                member=member,
                defaults={
                    "entry_type": "MEMBER",
                    "checkin_method": "QR",
                    "check_in_time": timezone.now(),
                }
            )

            # Already has a coupon?
            coupon = EventCoupon.objects.filter(
                attendance=attendance
            ).first()

            # Create coupon if it doesn't exist
            if not coupon:

                next_no = EventCoupon.objects.filter(
                    event=event
                ).count() + 1

                coupon = EventCoupon.objects.create(
                    event=event,
                    attendance=attendance,
                    coupon_no=f"C{next_no:04d}",
                    lucky_draw_no=f"{next_no:04d}",
                )

                attendance.coupon_issued = True
                attendance.save()

            # Print coupon
            messages.success(
                request,
                "Check-in successful. Please collect your coupon from the registration desk."
            )

            return render(
                request,
                "events/member_entry_success.html",
                {
                    "event": event,
                    "member": member,
                    "attendance": attendance,
                }
            )


        else:

            messages.warning(
                request,
                "Mobile Number / Membership Number not found. Please fill in the visitor details below."
            )

            return render(
                request,
                "events/visitor_register.html",
                {
                    "event": event,
                    "mobile": search_no
                }
            )


    return render(
        request,
        "events/agm_entry.html",
        {
            "event":event
        }
    )


def visitor_save(request,event_id):

    event=get_object_or_404(
        Event,
        id=event_id
    )


    if request.method=="POST":


        attendance=EventAttendance.objects.create(
            event=event,
            member=None,
            entry_type="VISITOR",
            checkin_method="QR",
            check_in_time=timezone.now()
        )


        visitor=EventVisitor.objects.create(

            event=event,

            visitor_name=request.POST.get(
                "visitor_name"
            ),

            mobile=request.POST.get(
                "mobile"
            ),

            company=request.POST.get(
                "company"
            ),

            city=request.POST.get(
                "city"
            ),

            email=request.POST.get(
                "email"
            ),

            referred_by=None,

            attendance=attendance
        )
        print("=" * 50)
        print("VISITOR SAVED")
        print("ID:", visitor.id)
        print("Name:", visitor.visitor_name)
        print("Mobile:", visitor.mobile)
        print("Total Visitors:", EventVisitor.objects.count())
        print("=" * 50)


        messages.success(
            request,
            "Registration successful. Please collect your visitor pass from the registration desk."
        )

        return render(
            request,
            "events/visitor_success.html",
            {
                "visitor": visitor,
            }
        )


@login_required(login_url="login")
def event_qr_print(request, id):

    event = get_object_or_404(Event, id=id)

    url = f"https://membership-erp.onrender.com/events/agm-entry/{event.id}/"

    img = qrcode.make(url)

    buffer = BytesIO()
    img.save(buffer, format="PNG")

    qr = base64.b64encode(buffer.getvalue()).decode()

    return render(
        request,
        "events/event_qr_print.html",
        {
            "event": event,
            "qr": qr,
            "url": url,
        },
    )


@login_required(login_url="login")
def print_queue(request):

    members = EventCoupon.objects.select_related(
        "attendance__member"
    ).order_by("-issued_at")

    visitors = EventVisitor.objects.order_by("-created_at")

    member_waiting = EventCoupon.objects.filter(printed=False).count()
    visitor_waiting = EventVisitor.objects.filter(printed=False).count()

    waiting_count = member_waiting + visitor_waiting

    member_printed = EventCoupon.objects.filter(printed=True).count()
    visitor_printed = EventVisitor.objects.filter(printed=True).count()

    printed_count = member_printed + visitor_printed

    return render(
        request,
        "events/print_queue.html",
        {
            "members": members,
            "visitors": visitors,
            "waiting_count": waiting_count,
            "printed_count": printed_count,
        }
    )
@login_required(login_url="login")
def visitor_pass_print(request, id):

    visitor = get_object_or_404(
        EventVisitor.objects.select_related(
            "event",
            "attendance"
        ),
        id=id
    )

    # Mark as printed
    if not visitor.printed:
        visitor.printed = True
        visitor.printed_at = timezone.now()
        visitor.save(update_fields=["printed", "printed_at"])

    return render(
        request,
        "events/visitor_pass_print.html",
        {
            "visitor": visitor
        }
    )



@login_required(login_url="login")
def agm_reports(request):

    total_events = Event.objects.count()

    total_members = EventAttendance.objects.filter(
        entry_type="MEMBER"
    ).count()

    total_visitors = EventAttendance.objects.filter(
        entry_type="VISITOR"
    ).count()

    total_attendance = EventAttendance.objects.count()

    member_printed = EventCoupon.objects.filter(
        printed=True
    ).count()

    member_waiting = EventCoupon.objects.filter(
        printed=False
    ).count()

    visitor_printed = EventVisitor.objects.filter(
        printed=True
    ).count()

    visitor_waiting = EventVisitor.objects.filter(
        printed=False
    ).count()

    context = {
        "total_events": total_events,
        "total_members": total_members,
        "total_visitors": total_visitors,
        "total_attendance": total_attendance,
        "member_printed": member_printed,
        "member_waiting": member_waiting,
        "visitor_printed": visitor_printed,
        "visitor_waiting": visitor_waiting,
    }

    return render(
        request,
        "events/agm_reports.html",
        context
    )


@login_required(login_url="login")
def member_attendance_report(request):

    members = EventCoupon.objects.select_related(
        "attendance__member",
        "event"
    ).order_by("-issued_at")

    events = Event.objects.all().order_by("-event_date")

    event = request.GET.get("event")
    search = request.GET.get("search")

    # Event Filter
    if event:
        members = members.filter(event_id=event)

    # Search Filter
    if search:
        members = members.filter(
            Q(attendance__member__membership_no__icontains=search) |
            Q(attendance__member__owner_name__icontains=search) |
            Q(attendance__member__mobile__icontains=search)
        )

    context = {
        "members": members,
        "events": events,
        "selected_event": event,
        "search": search,
    }

    return render(
        request,
        "events/member_attendance_report.html",
        context,
    )

@login_required(login_url="login")
def visitor_report(request):

    visitors = EventVisitor.objects.select_related(
        "event"
    ).order_by("-created_at")

    events = Event.objects.all().order_by("-event_date")

    event = request.GET.get("event")
    search = request.GET.get("search")

    if event:
        visitors = visitors.filter(event_id=event)

    if search:
        visitors = visitors.filter(
            Q(visitor_name__icontains=search) |
            Q(mobile__icontains=search) |
            Q(company__icontains=search) |
            Q(city__icontains=search)
        )

    return render(
        request,
        "events/visitor_report.html",
        {
            "visitors": visitors,
            "events": events,
            "selected_event": event,
            "search": search,
        },
    )


@login_required(login_url="login")
def member_attendance_print(request):

    members = EventCoupon.objects.select_related(
        "attendance__member",
        "event"
    ).order_by("-issued_at")

    return render(
        request,
        "events/member_attendance_print.html",
        {
            "members": members,
        },
    )


@login_required(login_url="login")
def visitor_report_print(request):

    visitors = EventVisitor.objects.select_related(
        "event",
        "attendance"
    ).order_by("-created_at")

    return render(
        request,
        "events/visitor_report_print.html",
        {
            "visitors": visitors,
        }
    )


def member_count(request):
    members = Member.objects.order_by("-id")[:20]

    html = f"Total Members: {Member.objects.count()}<br><br>"

    for m in members:
        html += f"{m.id} - {m.owner_name}<br>"

    return HttpResponse(html)



def db_check(request):
    db = settings.DATABASES["default"]
    return HttpResponse(
        f"""
        ENGINE: {db['ENGINE']}<br>
        NAME: {db['NAME']}<br>
        HOST: {db.get('HOST', '')}<br>
        """
    )

