from django.contrib import admin

from django.contrib import admin
from .models import Pharma
from .models import Seller
from .models import Approval
from .models import Categories
from .models import popular
from .models import cart

admin.site.register(cart)
admin.site.register(popular)
admin.site.register(Categories)
admin.site.register(Approval)
admin.site.register(Pharma)
admin.site.register(Seller)


# Register your models here.
