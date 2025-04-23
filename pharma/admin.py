from django.contrib import admin

from django.contrib import admin
from .models import Pharma
from .models import Seller
from .models import Approval

admin.site.register(Approval)
admin.site.register(Pharma)
admin.site.register(Seller)


# Register your models here.
