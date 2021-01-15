from django.contrib import admin
from .models import AvatarImage, Image, SOBE_Users, Regions, Categories, Lots, Sellers, Dealings

admin.site.register(AvatarImage)
admin.site.register(Image)
admin.site.register(SOBE_Users)
admin.site.register(Regions)
admin.site.register(Categories)
admin.site.register(Lots)
admin.site.register(Sellers)
admin.site.register(Dealings)