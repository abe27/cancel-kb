from collections.abc import Callable
from typing import Any
from django.contrib import admin, messages
from django.conf import settings
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html
import datetime
import requests

from joborder.models import JobOrder, JobToTrack, Track, TrackPL


# Register your models here.
class JobOrderAdmin(admin.ModelAdmin):
    change_form_template = "admin/change_form_joborder.html"
    list_display = (
        "open_dates",
        "job_no",
        "part_no",
        "plant",
        "qty",
        "mtm_dates",
        "rmtm_dates",
        # "user_id",
        "is_status",
    )

    list_filter = (
        "open_date",
        "mtm_date",
        "rmtm_date",
        "status",
    )

    readonly_fields = (
        "open_date",
        "job_no",
        "part_no",
        "plant",
        "qty",
        "mtm_date",
        "rmtm_date",
        "user_id",
        "status",
    )

    search_fields = (
        "job_no",
        "part_no",
    )

    list_per_page = 25

    def open_dates(self, obj):
        if obj.open_date:
            return obj.open_date.strftime("%Y-%m-%d")
        return obj.open_date

    open_dates.short_description = "Open Date"

    def mtm_dates(self, obj):
        if obj.mtm_date:
            return obj.mtm_date.strftime("%Y-%m-%d %H:%M")
        return obj.mtm_date

    mtm_dates.short_description = "MTM Date"

    def rmtm_dates(self, obj):
        if obj.rmtm_date:
            return obj.rmtm_date.strftime("%Y-%m-%d %H:%M")
        return obj.rmtm_date

    rmtm_dates.short_description = "RMTM Date"

    def is_status(self, obj):
        if obj.status == 1:
            return format_html("<span class='text-primary'>แสกนแล้ว</span>")

        if obj.status == 2:
            return format_html("<span class='text-primary'>ยกเลิกแล้ว</span>")
        return format_html("<span class='text-bold'>-</span>")

    is_status.short_description = "Status"

    def message_user(
        self, request, message, level=messages.INFO, extra_tags="", fail_silently=True
    ):
        pass

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["object_id"] = object_id
        return super().change_view(request, object_id, form_url, extra_context)

    def get_queryset(self, request):
        return super().get_queryset(request)

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def delete_model(self, request, obj):
        # if obj.status == 1:
        #     messages.error(request, "ไม่สามารถยกเลิกรายการนี้ได้เนื่องจากมีการยกเลิกแล้ว",fail_silently=True)
        #     return

        ### Update Tags
        Track.objects.filter(job_no=obj.job_no).update(
            end_date=datetime.datetime.now(),
            user_id=None,
            act_start_date=datetime.datetime.now(),
            status=1,
        )

        ### Update JOTOORDER
        JobToTrack.objects.filter(job_no=obj.job_no).update(status=1)

        ### UPDATE JOBORDER
        obj.mtm_date = datetime.datetime.now()
        obj.user_id = None
        obj.status = 1
        obj.rmtm_date = datetime.datetime.now()
        obj.save()
        ### Alert Line notify
        msg = f"message=เรียนทุกท่าน\nขณะนี้ระบบได้ทำการยกเลิกเอกสาร\nเลขที่ {str(obj.job_no).strip()}\nเรียบร้อยแล้วคะ"

        try:
            url = "https://notify-api.line.me/api/notify"
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Bearer {settings.LINE_NOTIFY_TOKEN}",
            }

            requests.request("POST", url, headers=headers, data=msg.encode("utf-8"))
        except:
            pass
        messages.success(
            request,
            f"อัพเดทข้อมูล {str(obj.job_no).strip()} เรียบร้อยแล้ว",
            fail_silently=True,
        )
        # return super().delete_model(request, obj)

    pass


class JobToTrackAdmin(admin.ModelAdmin):
    pass


class TrackAdmin(admin.ModelAdmin):
    change_form_template = "admin/change_form_track.html"
    list_display = (
        "job_no",
        "part_no",
        "kanban_id",
        "start_dates",
        "end_dates",
        "work_name",
        "status",
    )
    readonly_fields = (
        "kanban_id",
        "part_no",
        "step",
        "work_name",
        "ct",
        "ac_ct",
        "start_date",
        "end_date",
        "user_id",
        "status",
        "act_start_date",
        "job_no",
        "stop_date",
        "stop_ct",
        "type_user",
        "factory",
        "sup_code",
        "pvf_start_date",
        "pvf_end_date",
    )
    search_fields = ("job_no", "part_no", "kanban_id")
    list_display_links = None
    list_per_page = 25

    def start_dates(self, obj):
        if obj.start_date:
            return obj.start_date.strftime("%Y-%m-%d %H:%M")
        return obj.start_date

    start_dates.short_description = "Start Date"

    def end_dates(self, obj):
        if obj.end_date:
            return obj.end_date.strftime("%Y-%m-%d %H:%M")
        return obj.end_date

    end_dates.short_description = "End Date"

    def has_delete_permission(self, request, obj=None):
        return False

    pass


class TrackPLAdmin(admin.ModelAdmin):
    search_fields = [
        "kanban_id",
        "job_no",
        "part_no",
    ]
    list_display = [
        # "kanban_id",
        "job_no",
        "part_no",
        "track_id",
        "_start_date",
        "_end_date",
        # "step",
        "_status",
    ]

    def _start_date(self, obj):
        return (obj.start_date).strftime("%Y-%m-%d")

    _start_date.short_description = "Start Date"

    def _end_date(self, obj):
        if obj.end_date:
            return (obj.end_date).strftime("%Y-%m-%d")
        return "-"

    _end_date.short_description = "End Date"

    def _status(self, obj):
        if obj.status == 0:
            return format_html(f"<strong style='color:green;'>PL แสกนแล้ว</strong>")

        return format_html(f"<strong style='color:red;'>ยังไม่แสกน PL</strong>")

    _status.short_description = "Status"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.order_by("kanban_id", "job_no", "part_no")
        return queryset

    list_per_page = 25

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    pass


admin.site.register(JobOrder, JobOrderAdmin)
# admin.site.register(JobToTrack, JobToTrackAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(TrackPL, TrackPLAdmin)
