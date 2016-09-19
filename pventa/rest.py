from venta import models as venta
from restorant import models as restorant
from django.contrib.auth.models import User
from venta.models import Service
from cuser.middleware import CuserMiddleware
from rest_framework import routers, serializers, viewsets
from rest_framework import routers, viewsets, filters, generics, renderers
from django.contrib.auth import login, logout
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.http import HttpResponse
import json

class AuthView(generic.View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except:
            data = request.POST
        #end try
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None and user.is_authenticated():
            login(request, user)
            return HttpResponse()
        #end if
        return HttpResponse(status=400)
    #end def

    def delete(self, request):
        logout(request)
        return HttpResponse()
    #end def
#end end

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')
    #end class
#end class

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
#end class

class TableSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = restorant.Table
        fields = ('id','name', )
    #end class
#end class

class TableViewSet(viewsets.ModelViewSet):
    queryset = restorant.Table.objects.all()#exclude(settable__order__paid=False, settable__order__canceled=False)
    serializer_class = TableSerializer
#end class

class SetTableSerializer(serializers.HyperlinkedModelSerializer):
    table = serializers.PrimaryKeyRelatedField(queryset=restorant.Table.objects.all())
    order = serializers.PrimaryKeyRelatedField(queryset=venta.Order.objects.all())
    class Meta:
        model = restorant.SetTable
        fields = ('id','table', 'order')
    #end class
#end class

class SetTableViewSet(viewsets.ModelViewSet):
    queryset = restorant.SetTable.objects.all()
    serializer_class = SetTableSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('order__id',)
#end class

class PresentationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = venta.Presentation
        fields = ('id', 'name',  )
    #end class
    def create(self, validated_data):
        user = CuserMiddleware.get_user()
        service = venta.Service.objects.filter(userservice__user = user).first()
        validated_data['service'] = service
        return super(PresentationSerializer, self).create(validated_data)
    #end def
#end class

class PresentationViewSet(viewsets.ModelViewSet):
    queryset = venta.Presentation.objects.all()
    serializer_class = PresentationSerializer
    def get_queryset(self):
        user = CuserMiddleware.get_user()
        queryset = super(PresentationViewSet, self).get_queryset()
        queryset = queryset.filter(service__userservice__user = user)
        return queryset
    #end def
#end class

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=venta.Category.objects)
    presentation = serializers.PrimaryKeyRelatedField(queryset=venta.Presentation.objects)
    presentation_obj = PresentationSerializer(source="presentation", required=False)
    class Meta:
        model = venta.Product
        fields = ('id', 'category', 'presentation', 'presentation_obj','name', 'price',)
    #end class
#end class

class ProductViewSet(viewsets.ModelViewSet):
    queryset = venta.Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('category__id',)
    def get_queryset(self):
        user = CuserMiddleware.get_user()
        queryset = super(ProductViewSet, self).get_queryset()
        queryset = queryset.filter(category__service__userservice__user = user)
        return queryset
    #end def
#end class


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = venta.Image
        fields = ('id', 'name', 'url', )
    #end class
#end class

class ImageViewSet(viewsets.ModelViewSet):
    queryset = venta.Image.objects.all()
    serializer_class = ImageSerializer
    def get_queryset(self):
        user = CuserMiddleware.get_user()
        queryset = super(ImageViewSet, self).get_queryset()
        queryset = queryset.filter(service__userservice__user = user)
        return queryset
    #end def
#end class

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.PrimaryKeyRelatedField(queryset=venta.Image.objects)
    class Meta:
        model = venta.Category
        fields = ('id', 'name', 'image',)
    #end class
    def create(self, validated_data):
        user = CuserMiddleware.get_user()
        service = venta.Service.objects.filter(userservice__user = user).first()
        row = {
            'name': validated_data['name'],
            'service': service,
            'image': validated_data['image']
        }
        return venta.Category.objects.create(**row)
    #end def
#end class

# ViewSets define the view behavior.
class CategoryViewSet(viewsets.ModelViewSet):
    allowed_methods = ('GET', 'PUT', 'POST')
    queryset = venta.Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = ('id', )
    search_fields = ('name', )

    def get_queryset(self):
        user = CuserMiddleware.get_user()
        queryset = super(CategoryViewSet, self).get_queryset()
        queryset = queryset.filter(service__userservice__user = user)
        return queryset
    #end def
#end class

class ClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = venta.Client
        fields = ('cc', 'name', 'email', 'tel', )
    #end class
    def create(self, validated_data):
        user = CuserMiddleware.get_user()
        service = venta.Service.objects.filter(userservice__user = user).first()
        validated_data['service'] = service
        return super(ClientSerializer, self).create(validated_data);
    #end def
#end class

class ClientViewSet(viewsets.ModelViewSet):
    queryset = venta.Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = ('cc', )
    search_fields = ('name', 'tel')
    def get_queryset(self):
        user = CuserMiddleware.get_user()
        queryset = super(ClientViewSet, self).get_queryset()
        queryset = queryset.filter(service__userservice__user = user)
        return queryset
    #end def
#end class

class BillSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = venta.Bill
        fields = ('id','cc', 'name', 'tel', 'products', 'date', 'cash', 'check', 'card', 'disscount', 'paid', 'casher', 'waiter', 'tip', 'subtotal','iva', 'ipoconsumo','total', 'totaltip')
    #end class
    def create(self, validated_data):
        user = CuserMiddleware.get_user()
        service = venta.Service.objects.filter(userservice__user = user).first()
        validated_data['service'] = service
        validated_data['casher'] = user
        return super(BillSerializer, self).create(validated_data)
    #end def
#end class

# ViewSets define the view behavior.
class BillViewSet(viewsets.ModelViewSet):
    queryset = venta.Bill.objects.all()
    serializer_class = BillSerializer
    def get_queryset(self):
        user = CuserMiddleware.get_user()
        queryset = super(BillViewSet, self).get_queryset()
        queryset = queryset.filter(service__userservice__user = user)
        return queryset
    #end def
#end class

class ItemOrderSerializer(serializers.HyperlinkedModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=venta.Product.objects)
    product_obj = ProductSerializer(source="product",required=False)
    class Meta:
        model = venta.ItemOrder
        fields = ('product', 'product_obj', 'count',)
    #end class

#end class

# ViewSets define the view behavior.
class ItemOrderViewSet(viewsets.ModelViewSet):
    queryset = venta.ItemOrder.objects.all()
    serializer_class = ItemOrderSerializer
    def get_queryset(self):
        user = CuserMiddleware.get_user()
        queryset = super(ItemOrderViewSet, self).get_queryset()
        return queryset
    #end def

#end class

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    bill = serializers.PrimaryKeyRelatedField(queryset=venta.Bill.objects.all())
    table = serializers.SerializerMethodField()
    waiter = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(OrderSerializer, self).__init__(*args, **kwargs)
    #end def

    def get_waiter(self, obj):
        return obj.waiter.username
    #end def

    def get_table(self, obj):
        table = restorant.Table.objects.filter(settable__order = obj).first()
        if table:
            return table.name
        #end if
        return "Sin mesa"
    #end def

    products = ItemOrderSerializer(many=True)
    class Meta:
        model = venta.Order
        fields = ('id', 'client', 'products', 'date', 'bill', 'total', 'frienly_date', 'canceled', 'paid', 'table', 'waiter')
    #end class

    def validate(self, data):
        order = self.instance
        for item in order.products.all():
            total = item.product.total()
            if total < item.count and not hasattr(item.product, 'dish'):
                raise serializers.ValidationError("Error no hay suficiente %s para vender %d quedan solo %s" % (item.product.name, item.count, total))
            # end if
        # end for
        return data
    # end def

    def create(self, validated_data):
        user = CuserMiddleware.get_user()
        service = venta.Service.objects.filter(userservice__user = user).first()
        data = {}
        data['waiter'] = user
        if 'bill' in validated_data:
            data['bill'] = validated_data['bill']
        #end if
        if 'client' in validated_data:
            data['client']  = validated_data['client']
        #end if
        data['service'] = service
        order = venta.Order.objects.create(**data)
        for item in validated_data['products']:
            item['product'].sell(item['count'])
            itemorder = venta.ItemOrder.objects.create(product=item['product'], count=item['count'])
            order.products.add(itemorder)
        #end for
        return order
    #end def

    def update(self, instance, validated_data):
        if not instance:
            return self.create(validated_data)
        #end if
        user = CuserMiddleware.get_user()
        service = venta.Service.objects.filter(userservice__user = user).first()
        order = instance
        if 'bill' in validated_data:
            order.bill = validated_data['bill']
        #end if
        if 'client' in validated_data:
            order.client  = validated_data['client']
        #end if
        if 'canceled' in validated_data:
            order.canceled  = validated_data['canceled']
        #end if
        if 'paid' in validated_data:
            order.casher = user
            order.paid = validated_data['paid']
        #end if
        order.service = service
        order.save()
        print "update", validated_data
        if 'products' in validated_data:
            order.products.all().delete()
            for item in validated_data['products']:
                itemorder = venta.ItemOrder.objects.create(product=item['product'], count=item['count'])
                order.products.add(itemorder)
            #end for
        #end if
        if order.canceled:
            restorant.Consumption.objects.filter(order=order).update(canceled=True)
        elif order.paid:

            user = CuserMiddleware.get_user()
            service = venta.Service.objects.filter(userservice__user = user).first()
            client, created = venta.Client.objects.get_or_create(cc=order.bill.cc, name=order.bill.name, tel=order.bill.tel, service=service)
            order.client = client
            order.save()
            for item in order.products.all():
                item.product.sell(item.count)
                comps = restorant.ConsumptionDish.objects.filter(dish=item.product)
                if comps.count():# Es un plato
                    for comp in comps:
                        supply = comp.supply.get_buy_supply()
                        if supply:
                            restorant.Consumption.objects.create(product=comp.dish, supply=supply, consumption=comp.consumption, order=order)
                            supply.current_count = supply.current_count - comp.consumption
                            supply.save()
                        #end if
                    #end for
                else:#Es un producto
                    product = item.product.get_buy_product()
                    if product:
                        print "menos ", item.count
                        product.current_count = product.current_count - item.count
                        product.save()
                    #end if
                #end if
            #end for
        #end def
        return order
    #end def

#end class

class OrderViewSet(viewsets.ModelViewSet):
    queryset = venta.Order.objects.filter(canceled=False)
    serializer_class = OrderSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = ('id', 'paid')
    search_fields = ('client__name', 'product__name')
    def get_queryset(self):
        user = CuserMiddleware.get_user()
        queryset = super(OrderViewSet, self).get_queryset()
        queryset = queryset.filter(service__userservice__user = user)
        return queryset
    #end def

#end class

class PendantTableSerializer(serializers.HyperlinkedModelSerializer):
    order = OrderSerializer(required=False)
    table = TableSerializer(required=False)
    class Meta:
        model = restorant.Table
        fields = ('id','table', 'order')
    #end class
    def get_queryset(self):
        user = CuserMiddleware.get_user()
        queryset = super(PendantTableSerializer, self).get_queryset()
        queryset = queryset.filter(service__userservice__user = user)
        return queryset
    #end def

#end class


# ViewSets define the view behavior.
class PendantTableViewSet(viewsets.ModelViewSet):
    queryset = restorant.SetTable.objects.filter(order__paid=False, order__canceled=False)
    serializer_class = PendantTableSerializer
#end class


from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'categorys', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'bills', BillViewSet)
router.register(r'itemorders', ItemOrderViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'images', ImageViewSet)
router.register(r'presentation', PresentationViewSet)
router.register(r'tables', TableViewSet)
router.register(r'pendant', PendantTableViewSet)
router.register(r'settable', SetTableViewSet)

config = {
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
}

urlpatterns = ([
    url(r'^', include(router.urls)),
    url(r'^users/(?P<pk>(\d+))/$', UserViewSet.as_view(config)),
    url(r'^categorys/(?P<pk>(\d+))/$', CategoryViewSet.as_view(config)),
    url(r'^products/(?P<pk>(\d+))/$', ProductViewSet.as_view(config)),
    url(r'^clients/(?P<pk>(\d+))/$', ClientViewSet.as_view(config)),
    url(r'^bills/(?P<pk>(\d+))/$', BillViewSet.as_view(config)),
    url(r'^itemorders/(?P<pk>(\d+))/$', ItemOrderViewSet.as_view(config)),
    url(r'^orders/(?P<pk>(\d+))/$', OrderViewSet.as_view(config)),
    url(r'^images/(?P<pk>(\d+))/$', ImageViewSet.as_view(config)),
    url(r'^presentation/(?P<pk>(\d+))/$', PresentationViewSet.as_view(config)),
    url(r'^settable/(?P<pk>(\d+))/$', SetTableViewSet.as_view(config)),
])
