from typing import Any
from django.contrib import admin,messages
from django.conf import settings
from django.utils.html import format_html
import datetime
import requests

from joborder.models import JobOrder, JobToTrack, Track


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
        "user_id",
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

        return format_html("<span class='text-bold'>-</span>")

    is_status.short_description = "Status"

    def message_user(self, request, message, level=messages.INFO, extra_tags='', fail_silently=False):
        pass

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["object_id"] = object_id
        return super().change_view(request, object_id, form_url, extra_context)

    def delete_model(self, request, obj):
        ### Update Tags
        track = Track.objects.filter(job_no=obj.job_no)
        for r in track:
            r.end_date = datetime.datetime.now()
            r.user_id = None
            r.act_start_date = datetime.datetime.now()
            r.save()

        ### Update JOTOORDER
        jobs = JobToTrack.objects.filter(job_no=obj.job_no)
        for r in jobs:
            r.status = 1
            r.save()

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
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Bearer {settings.LINE_NOTIFY_TOKEN}'
            }

            response = requests.request("POST", url, headers=headers, data=msg.encode("utf-8"))
            print(response.text)
        except:
            pass
        # messages.success(request, msg)
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


admin.site.register(JobOrder, JobOrderAdmin)
# admin.site.register(JobToTrack, JobToTrackAdmin)
admin.site.register(Track, TrackAdmin)
