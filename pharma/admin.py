from django.contrib import admin

from django.contrib import admin
from .models import Pharma
from .models import Seller
from .models import Approval
from .models import Categories
from .models import popular
from .models import cart
from .models import buyerinfo
from .models import Payment
from .models import Pending_payment
from .models import paymentmethod
from .models import bought
from .models import boughtitem
from .models import help

admin.site.register(help)
admin.site.register(boughtitem)
#admin.site.register(bought)
admin.site.register(paymentmethod)
admin.site.register(Payment)
admin.site.register(Pending_payment)
admin.site.register(buyerinfo)
admin.site.register(cart)
admin.site.register(popular)
admin.site.register(Categories)
admin.site.register(Approval)
admin.site.register(Pharma)
admin.site.register(Seller)



# Register your models here.
