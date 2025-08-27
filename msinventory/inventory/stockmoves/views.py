from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import StockMove, StockMoveLine
from .serializers import StockMoveSerializer, StockMoveCreateSerializer
from utils.exceptions import InsufficientStockException

class StockMoveViewSet(viewsets.ModelViewSet):
    queryset = StockMove.objects.all().select_related('from_location', 'to_location').prefetch_related('lines__product')
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return StockMoveCreateSerializer
        return StockMoveSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            with transaction.atomic():
                lines_data = serializer.validated_data.pop('lines', [])
                stock_move = StockMove.objects.create(**serializer.validated_data, completed=True)
                
                for line_data in lines_data:
                    StockMoveLine.objects.create(stock_move=stock_move, **line_data)
                
                stock_move.execute_move()
                
                response_serializer = StockMoveSerializer(stock_move)
                
                headers = self.get_success_headers(serializer.data)
                return Response(
                    response_serializer.data, 
                    status=status.HTTP_201_CREATED, 
                    headers=headers
                )
        except ValueError as e:
            if "Insufficient stock" in str(e):
                raise InsufficientStockException()
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        if instance.completed:
            return Response(
                {'error': 'Cannot update a completed stock move'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        try:
            with transaction.atomic():
                self.perform_update(serializer)
                
                if instance.completed:
                    instance.execute_move()
                
                return Response(serializer.data)
                
        except ValueError as e:
            if "Insufficient stock" in str(e):
                raise InsufficientStockException()
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def perform_update(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        move = self.get_object()
        
        if move.completed:
            return Response(
                {'error': 'Move is already completed'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            with transaction.atomic():
                move.completed = True
                move.save() 
                return Response({'message': 'Move completed successfully'})
        except ValueError as e:
            if "Insufficient stock" in str(e):
                raise InsufficientStockException()
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def by_product(self, request):
        product_id = request.query_params.get('product_id')
        if not product_id:
            return Response(
                {'error': 'product_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        moves = StockMove.objects.filter(lines__product_id=product_id).distinct()
        serializer = self.get_serializer(moves, many=True)
        return Response(serializer.data)