from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from orders.serializers import (
    ItemSerializer,
    MakeOrderSerializer,
    MealSerializer,
    OrderSerializer
)
# Create your views here.
class ItemListView(ListAPIView):
    """
    Lists all the food items available.
    """
    serializer_class = ItemSerializer
    permission_classes = []
    queryset = ItemSerializer.Meta.model.objects.all()


class MealListView(ListAPIView):
    """
    Lists all the meals available.
    Meals are made up of items available.
    """
    serializer_class = MealSerializer
    permission_classes = []
    queryset = MealSerializer.Meta.model.objects.all()


class OrderListView(ListAPIView):
    """
    Lists all the orders made by the requesting user. 
    If the user is a superuser, a list of all orders is returned.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = OrderSerializer.Meta.model.objects.all()

    def get(self, request):
        if request.user.is_superuser:
            data = OrderSerializer(self.get_queryset(), many=True).data
            return Response(data)

        data = OrderSerializer(
            OrderSerializer.Meta.model.objects.filter(
                user=request.user
            ),
            many=True,
        ).data
        return Response(data)


class MakeOrderView(GenericAPIView):
    """
    Makes an order for the requesting user.
    The user can order items or meals.
    A reference to the payment for the intended order is also required to make the order.
    """
    serializer_class = MakeOrderSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid()
        serializer.save()
        message, status, order = serializer.save()
        return Response(data={"message": message, "order":order}, status=status)

#TODO CancelOrderView
#TODO Accept/RejectView
