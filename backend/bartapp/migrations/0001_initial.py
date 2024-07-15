# Generated by Django 5.0.7 on 2024-07-15 21:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Agency",
            fields=[
                ("agency_id", models.TextField(primary_key=True, serialize=False)),
                ("agency_name", models.TextField()),
                ("agency_url", models.URLField()),
                ("agency_timezone", models.TextField(null=True)),
                ("agency_lang", models.TextField(null=True)),
                ("agency_phone", models.TextField()),
            ],
            options={
                "db_table": "agency",
            },
        ),
        migrations.CreateModel(
            name="Calendar",
            fields=[
                ("service_id", models.TextField(primary_key=True, serialize=False)),
                ("monday", models.IntegerField()),
                ("tuesday", models.IntegerField()),
                ("wednesday", models.IntegerField()),
                ("thursday", models.IntegerField()),
                ("friday", models.IntegerField()),
                ("saturday", models.IntegerField()),
                ("sunday", models.IntegerField()),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
            ],
            options={
                "db_table": "calendar",
            },
        ),
        migrations.CreateModel(
            name="FareAttribute",
            fields=[
                ("fare_id", models.IntegerField(primary_key=True, serialize=False)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("currency_type", models.TextField()),
                ("payment_method", models.IntegerField()),
                ("transfers", models.IntegerField(null=True)),
                ("transfer_duration", models.IntegerField(null=True)),
            ],
            options={
                "db_table": "fare_attributes",
            },
        ),
        migrations.CreateModel(
            name="FeedInfo",
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
                ("feed_publisher_name", models.TextField()),
                ("feed_publisher_url", models.URLField()),
                ("feed_lang", models.TextField()),
                ("feed_start_date", models.DateField()),
                ("feed_end_date", models.DateField()),
                ("feed_version", models.TextField()),
            ],
            options={
                "db_table": "feed_info",
            },
        ),
        migrations.CreateModel(
            name="RiderCategory",
            fields=[
                (
                    "rider_category_id",
                    models.IntegerField(primary_key=True, serialize=False),
                ),
                ("rider_category_description", models.TextField()),
            ],
            options={
                "db_table": "rider_categories",
            },
        ),
        migrations.CreateModel(
            name="Route",
            fields=[
                ("route_id", models.TextField(primary_key=True, serialize=False)),
                ("route_short_name", models.TextField()),
                ("route_long_name", models.TextField(null=True)),
                ("route_desc", models.TextField()),
                ("route_type", models.IntegerField()),
                ("route_url", models.URLField(null=True)),
                ("route_color", models.TextField()),
                ("route_text_color", models.TextField()),
            ],
            options={
                "db_table": "routes",
            },
        ),
        migrations.CreateModel(
            name="RTAlert",
            fields=[
                ("alert_id", models.IntegerField(primary_key=True, serialize=False)),
                ("info", models.TextField()),
                ("lang", models.TextField()),
            ],
            options={
                "db_table": "rt_alerts",
            },
        ),
        migrations.CreateModel(
            name="RTStopTimeUpdate",
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
                ("trip_id", models.IntegerField()),
                ("stop_id", models.TextField()),
                ("arrival_delay", models.IntegerField()),
                ("arrival_time", models.IntegerField()),
                ("arrival_uncertainty", models.IntegerField()),
                ("departure_delay", models.IntegerField()),
                ("departure_time", models.IntegerField()),
                ("departure_uncertainty", models.IntegerField()),
            ],
            options={
                "db_table": "rt_stop_time_updates",
            },
        ),
        migrations.CreateModel(
            name="RTTrip",
            fields=[
                ("trip_id", models.IntegerField(primary_key=True, serialize=False)),
                ("schedule_relationship", models.TextField()),
                ("vehicle", models.TextField()),
            ],
            options={
                "db_table": "rt_trips",
            },
        ),
        migrations.CreateModel(
            name="Stop",
            fields=[
                ("stop_id", models.TextField(primary_key=True, serialize=False)),
                ("stop_code", models.TextField(null=True)),
                ("stop_name", models.TextField()),
                ("stop_desc", models.TextField(null=True)),
                ("stop_lat", models.TextField()),
                ("stop_lon", models.TextField()),
                ("zone_id", models.TextField(null=True)),
                ("plc_url", models.URLField(null=True)),
                ("location_type", models.IntegerField()),
                ("parent_station", models.TextField(null=True)),
            ],
            options={
                "db_table": "stops",
            },
        ),
        migrations.CreateModel(
            name="Transfer",
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
                ("from_stop_id", models.TextField()),
                ("to_stop_id", models.TextField()),
                ("transfer_type", models.IntegerField(null=True)),
                ("min_transfer_time", models.IntegerField(null=True)),
                ("from_route_id", models.TextField(null=True)),
                ("to_route_id", models.TextField(null=True)),
                ("from_trip_id", models.TextField(null=True)),
                ("to_trip_id", models.TextField(null=True)),
            ],
            options={
                "db_table": "transfers",
            },
        ),
        migrations.CreateModel(
            name="Trip",
            fields=[
                ("route_id", models.TextField(null=True)),
                ("service_id", models.TextField(null=True)),
                ("trip_id", models.IntegerField(primary_key=True, serialize=False)),
                ("trip_headsign", models.TextField()),
                ("direction_id", models.TextField()),
                ("block_id", models.TextField()),
                ("shape_id", models.TextField()),
            ],
            options={
                "db_table": "trips",
            },
        ),
        migrations.CreateModel(
            name="CalendarAttribute",
            fields=[
                (
                    "service_id",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="bartapp.calendar",
                    ),
                ),
                ("service_description", models.TextField(max_length=255)),
            ],
            options={
                "db_table": "calendar_attributes",
            },
        ),
        migrations.CreateModel(
            name="CalendarDate",
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
                ("date", models.DateField()),
                ("exception_type", models.IntegerField()),
                (
                    "service_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bartapp.calendar",
                    ),
                ),
            ],
            options={
                "db_table": "calendar_dates",
            },
        ),
        migrations.CreateModel(
            name="FareRule",
            fields=[
                (
                    "fare_id",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="bartapp.fareattribute",
                    ),
                ),
                ("route_id", models.TextField(null=True)),
                ("origin_id", models.TextField()),
                ("destination_id", models.TextField()),
                ("contains_id", models.TextField(null=True)),
            ],
            options={
                "db_table": "fare_rules",
            },
        ),
        migrations.CreateModel(
            name="FareRiderCategory",
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
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "fare_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bartapp.fareattribute",
                    ),
                ),
                (
                    "rider_category_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bartapp.ridercategory",
                    ),
                ),
            ],
            options={
                "db_table": "fare_rider_categories",
            },
        ),
        migrations.CreateModel(
            name="RealtimeRoute",
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
                ("realtime_enabled", models.BooleanField()),
                ("realtime_routename", models.TextField(null=True)),
                ("realtime_routecode", models.TextField(null=True)),
                (
                    "route_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="bartapp.route"
                    ),
                ),
            ],
            options={
                "db_table": "realtime_routes",
            },
        ),
        migrations.CreateModel(
            name="Direction",
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
                ("direction_id", models.TextField()),
                ("direction", models.TextField()),
                (
                    "route_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="bartapp.route"
                    ),
                ),
            ],
            options={
                "db_table": "directions",
            },
        ),
        migrations.CreateModel(
            name="RouteAttribute",
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
                ("category", models.TextField()),
                ("subcategory", models.TextField()),
                ("running_way", models.TextField()),
                (
                    "route_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="bartapp.route"
                    ),
                ),
            ],
            options={
                "db_table": "route_attributes",
            },
        ),
        migrations.CreateModel(
            name="StopTime",
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
                ("arrival_time", models.TextField()),
                ("departure_time", models.TextField()),
                ("stop_sequence", models.IntegerField(null=True)),
                ("pickup_type", models.IntegerField(null=True)),
                ("drop_off_type", models.IntegerField(null=True)),
                ("shape_distance_traveled", models.IntegerField()),
                (
                    "stop_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="bartapp.stop"
                    ),
                ),
                (
                    "trip_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="bartapp.trip"
                    ),
                ),
            ],
            options={
                "db_table": "stop_times",
            },
        ),
        migrations.CreateModel(
            name="Shape",
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
                ("shape_pt_lat", models.IntegerField()),
                ("shape_pt_lon", models.IntegerField()),
                ("shape_pt_sequence", models.IntegerField()),
                ("shape_dist_traveled", models.IntegerField()),
                (
                    "shape_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="bartapp.trip"
                    ),
                ),
            ],
            options={
                "db_table": "shapes",
            },
        ),
    ]
