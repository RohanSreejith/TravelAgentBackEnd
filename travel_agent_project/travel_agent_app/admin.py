from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TravelAgent, Website, TravelPackage, ScrapedPackage, PackageMedia

class TravelAgentAdmin(UserAdmin):
    list_display = ('username', 'email', 'agency_name', 'phone_number', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Travel Agent Info', {'fields': ('phone_number', 'agency_name')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Travel Agent Info', {'fields': ('phone_number', 'agency_name', 'email')}),
    )

class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'agent', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'url', 'agent__username')

class PackageMediaInline(admin.TabularInline):
    model = PackageMedia
    extra = 1

class TravelPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'duration_days', 'price', 'agent')
    list_filter = ('destination',)
    search_fields = ('title', 'destination', 'agent__username')
    inlines = [PackageMediaInline]

class ScrapedPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'source_website', 'price', 'agent')
    list_filter = ('source_website', 'destination')
    search_fields = ('title', 'destination', 'agent__username')

admin.site.register(TravelAgent, TravelAgentAdmin)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(TravelPackage, TravelPackageAdmin)
admin.site.register(ScrapedPackage, ScrapedPackageAdmin)
admin.site.register(PackageMedia)