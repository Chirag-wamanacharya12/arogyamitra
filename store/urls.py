from django.urls import path
from .import views
from .webhooks import paypal_webhook

urlpatterns = [
    path('store/',views.store,name="store"), 
    path('viewProduct/<int:primary_id>/', views.viewProduct, name='viewProduct'),
    path('viewProduct/<int:primary_id>/<int:sub_id>/', views.viewProduct, name='viewProductSub'),
    # path('add-product/', views.add_product, name='add_product'),
    path('addToCart/<int:id>/',views.addToCart, name='addToCart'),
    path('cart/',views.viewCart,name='cart'),
    path('updateqty/<qv>/<int:id>/',views.updateQty),
    path('savedForLater/<int:id>/',views.savedForLater ,name='savedForLater'),
    path('removedFromSaved/<int:id>/',views.removeFromSaved,name='removedFromSaved'),
    path('deleteFromCart/<int:id>/',views.deleteFromCart,name='deleteFromCart'),
    path('viewDetails/<int:id>/',views.productDetails,name='viewDetails'),
    path('checkedToProceed/<int:id>/',views.checkedToProceed,name='checkedToProceed'),
    path('uncheckedToProceed/<int:id>/',views.uncheckedToProceed,name='uncheckedToProceed'), 
    path('productList/', views.productList, name='productList'),
    path("paypal-webhook/", paypal_webhook, name="paypal_webhook"),
    path('medication', views.medication, name='medication'),
    path('medication', views.medication, name='medication'),
    path('submit_address/', views.submit_address, name='submit_address'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_cancel/', views.payment_cancel, name='payment_cancel'),
]