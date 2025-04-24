from django.contrib import admin

from django.contrib import admin
from .models import Pharma
from .models import Seller
from .models import Approval
from .models import Categories


admin.site.register(Categories)
admin.site.register(Approval)
admin.site.register(Pharma)
admin.site.register(Seller)


# Register your models here.
