from django.contrib import admin
from .models import (
    Agency,
    FeedInfo,
    Route, 
    Stop, 
    Trip, 
    StopTime, 
    Calendar,
    CalendarAttribute,
    CalendarDate,
    FareAttribute, 
    FareRule, 
    RiderCategory, 
    FareRiderCategory,
    Shape, 
    RouteAttribute, 
    Direction, 
    Transfer,
    RealtimeRoute, 
)

# Register your models here.
admin.site.register(Route)
admin.site.register(Stop)
admin.site.register(Trip)
admin.site.register(StopTime)
admin.site.register(Agency)
admin.site.register(Calendar)

admin.site.register(FeedInfo)
admin.site.register(FareAttribute)
admin.site.register(FareRule)
admin.site.register(RiderCategory)
admin.site.register(FareRiderCategory)

admin.site.register(Shape)
admin.site.register(RouteAttribute)
admin.site.register(RealtimeRoute)
admin.site.register(Direction)
admin.site.register(Transfer)

admin.site.register(CalendarAttribute)
admin.site.register(CalendarDate)
