# Generated by Django 5.1 on 2024-08-14 10:10

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Apply",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("apply_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("company", models.CharField(max_length=10, null=True)),
                ("com_num", models.CharField(blank=True, max_length=14, null=True)),
                ("address_num", models.CharField(blank=True, max_length=5, null=True)),
                ("address_info", models.TextField(blank=True, null=True)),
                ("address_detail", models.TextField(blank=True, null=True)),
                ("deli_request", models.TextField(blank=True, null=True)),
                ("applicant", models.CharField(max_length=10, null=True)),
                ("apcan_phone", models.CharField(max_length=14, null=True)),
                (
                    "progress",
                    models.IntegerField(
                        choices=[
                            (0, "박스 요청중"),
                            (1, "박스 전송중"),
                            (2, "박스 수거 요청중"),
                            (3, "수거진행중"),
                            (4, "송장 입력 전"),
                        ],
                        default=0,
                        null=True,
                    ),
                ),
                ("box_num", models.IntegerField(null=True)),
                ("sent_box_num", models.IntegerField(null=True)),
                ("invoice_num", models.TextField(null=True)),
                ("zir_block_count", models.IntegerField(blank=True, null=True)),
                ("zir_powder_count", models.IntegerField(blank=True, null=True)),
                ("round_bar_count", models.IntegerField(blank=True, null=True)),
                ("tool_count", models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="CompanyInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("count", models.PositiveIntegerField(default=1, null=True)),
                ("company", models.CharField(max_length=10, null=True, unique=True)),
                ("com_num", models.CharField(blank=True, max_length=14, null=True)),
                ("address_num", models.CharField(blank=True, max_length=5, null=True)),
                ("address_info", models.TextField(blank=True, null=True)),
                ("address_detail", models.TextField(blank=True, null=True)),
                ("recent_apply", models.DateTimeField(auto_now=True, null=True)),
                ("recent_employee", models.CharField(max_length=10, null=True)),
                ("latitude", models.FloatField(blank=True, null=True)),
                ("longitude", models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="DoneApply",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("company", models.CharField(max_length=10, null=True)),
                ("applicant", models.CharField(max_length=10, null=True)),
                ("apcan_phone", models.CharField(max_length=14, null=True)),
                ("done_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("box_num", models.IntegerField(null=True)),
            ],
        ),
    ]
