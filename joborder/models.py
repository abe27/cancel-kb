from django.db import models

# Create your models here.
class JobOrder(models.Model):
    id = models.IntegerField(db_column="ID",  primary_key=True, editable=False)
    part_no = models.TextField(max_length=50, db_column="PART_NO")
    plant = models.TextField(max_length=10, db_column="PLANT", blank=True, null=True)# PLANT nchar(10) COLLATE Thai_CI_AS NULL,
    qty = models.TextField(max_length=10, db_column="NQTY", blank=True, null=True)# NQTY nchar(10) COLLATE Thai_CI_AS NULL,
    open_date = models.DateTimeField(db_column="OPEN_DATE", blank=True, null=True)# OPEN_DATE datetime NULL,
    mtm_date = models.DateTimeField(db_column="MTM_DATE", blank=True, null=True)# MTM_DATE datetime NULL,
    user_id = models.IntegerField(db_column="USER_ID")# USER_ID int NULL,
    status = models.IntegerField(db_column="STATUS")# STATUS int NULL,
    rmtm_date = models.DateTimeField(db_column="RMTM_DATE")# RMTM_DATE datetime NULL,
    job_no = models.TextField(max_length=50, db_column="JOB_NO")

    def __str__(self):
        return self.job_no

    class Meta:
        db_table = "JOBORDER"
        app_label = "joborder"
        verbose_name = "ยกเลิก JOBORDER"
        verbose_name_plural = "ยกเลิก JOB ORDER"
        ordering = ('-open_date','status','-job_no')
        

class JobToTrack(models.Model):
    job_no = models.TextField(max_length=50, db_column="JOB_NO", primary_key=True, editable=False)
    kanban_id = models.TextField(max_length=500, db_column="KANBAN")# USER_ID int NULL,
    status = models.IntegerField(db_column="STATUS")# STATUS int NULL,

    def __str__(self):
        return self.kanban_id

    class Meta:
        db_table = "JOBTOTRACK"
        app_label = "joborder"

class Track(models.Model):
    kanban_id = models.TextField(max_length=200, db_column="KANBAN", primary_key=True, editable=False)
    part_no = models.TextField(max_length=30, db_column="CPART_NO")
    step = models.IntegerField(db_column="STEP")
    work_name = models.TextField(max_length=50, db_column="WORK_NAME")
    ct = models.IntegerField(db_column="CT")
    ac_ct =  models.TextField(max_length=50, db_column="AC_CT")# AC_CT nvarchar(50) COLLATE Thai_CI_AS NULL,
    start_date = models.DateTimeField(db_column="STARTDATE")# STARTDATE datetime NULL,
    end_date = models.DateTimeField(db_column="ENDDATE")# ENDDATE datetime NULL,
    user_id = models.IntegerField(db_column="USER_ID")
    status = models.IntegerField(db_column="STATUS")
    act_start_date = models.DateTimeField(db_column="ACT_STARTDATE")# ACT_STARTDATE datetime NULL,
    job_no = models.TextField(max_length=50, db_column="JOB_NO")
    stop_date = models.DateTimeField(db_column="STOPDATE")# STOPDATE datetime NULL,
    stop_ct = models.IntegerField(db_column="STOP_CT")# STATUS int NULL,STOP_CT int DEFAULT 0 NOT NULL,
    type_user = models.IntegerField(db_column="TYPE_USER")#TYPE_USER int DEFAULT 0 NOT NULL,
    factory = models.TextField(max_length=50, db_column="FACTORY")# FACTORY nchar(10) COLLATE Thai_CI_AS NULL,
    sup_code = models.TextField(max_length=50, db_column="SUPCODE")# SUPCODE nvarchar(50) COLLATE Thai_CI_AS NULL,
    pvf_start_date = models.DateTimeField(db_column="PVF_STAR_DATE")# PVF_STAR_DATE datetime NULL,
    pvf_end_date = models.DateTimeField(db_column="PVF_ENDDATE")# PVF_ENDDATE datetime NULL

    def __str__(self):
        return self.kanban_id

    class Meta:
        db_table = "TRACK"
        app_label = "joborder"
        verbose_name = "รายการ TRACK"
        verbose_name_plural = "รายการ TRACK"
        ordering = ('-job_no','step', 'start_date','-end_date')

class TrackPL(models.Model):
    kanban_id = models.TextField(max_length=200, db_column="KANBAN", primary_key=True, editable=False)
    job_no = models.TextField(max_length=50, db_column="JOB_NO")
    part_no = models.TextField(max_length=30, db_column="CPART_NO")
    start_date = models.DateTimeField(db_column="STARTDATE")# STARTDATE datetime NULL,
    end_date = models.DateTimeField(db_column="ENDDATE")# ENDDATE datetime NULL,
    step = models.IntegerField(db_column="STEP")
    status = models.IntegerField(db_column="STATUS")

    def __str__(self):
        return str(self.kanban_id).strip()
    
    def track_id(self):
        txtScan = None
        for i in range(0, 3):
            a = 0
            if i == 0:
                a = str(self.kanban_id).find(",")
                txtScan = str(self.kanban_id)[a + 1:]
            if i == 1:
                a = str(txtScan).find(",")
                txtScan = str(txtScan)[a + 1:]
            if i == 2:
                a = str(txtScan).find(",")
            
            txt = str(txtScan[a+1:])
            x = str(txt).find(",")
        return txt[:x]

    class Meta:
        db_table = "TRACKPL"
        app_label = "joborder"
        verbose_name = "รายการสถานะ TRACKPL"
        verbose_name_plural = "รายการสถานะ TRACKPL"
        ordering = ('-start_date','step',"kanban_id")
