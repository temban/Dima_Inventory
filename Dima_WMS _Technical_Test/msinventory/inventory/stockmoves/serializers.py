from rest_framework import serializers
from .models import StockMove, StockMoveLine
from inventory.products.serializers import ProductSerializer
from inventory.locations.serializers import LocationSerializer

class StockMoveLineSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_internal_reference = serializers.CharField(source='product.internal_reference', read_only=True)
    
    class Meta:
        model = StockMoveLine
        fields = '__all__'
        read_only_fields = ('stock_move',)  # Make stock_move read-only

class StockMoveLineCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMoveLine
        fields = ['product', 'quantity', 'description']

class StockMoveSerializer(serializers.ModelSerializer):
    from_location_name = serializers.CharField(source='from_location.name', read_only=True)
    to_location_name = serializers.CharField(source='to_location.name', read_only=True)
    lines = StockMoveLineSerializer(many=True, read_only=True)
    
    class Meta:
        model = StockMove
        fields = '__all__'
        read_only_fields = ('timestamp',)

class StockMoveCreateSerializer(serializers.ModelSerializer):
    lines = StockMoveLineCreateSerializer(many=True, required=False)
    
    class Meta:
        model = StockMove
        fields = ['move_type', 'from_location', 'to_location', 'reference', 'description', 'lines']
        read_only_fields = ('timestamp', 'completed')
    
    def validate(self, data):
        move_type = data.get('move_type')
        from_location = data.get('from_location')
        to_location = data.get('to_location')
        
        if move_type == 'INBOUND' and not to_location:
            raise serializers.ValidationError("INBOUND moves require a destination location")
        if move_type == 'OUTBOUND' and not from_location:
            raise serializers.ValidationError("OUTBOUND moves require a source location")
        if move_type == 'TRANSFER' and (not from_location or not to_location):
            raise serializers.ValidationError("TRANSFER moves require both source and destination locations")
        
        return data
    
    def create(self, validated_data):
        lines_data = validated_data.pop('lines', [])
        stock_move = StockMove.objects.create(**validated_data)
        
        for line_data in lines_data:
            StockMoveLine.objects.create(stock_move=stock_move, **line_data)
        
        return stock_move
    
    def update(self, instance, validated_data):
        lines_data = validated_data.pop('lines', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if lines_data is not None:
            instance.lines.all().delete()
            
            for line_data in lines_data:
                StockMoveLine.objects.create(stock_move=instance, **line_data)
        
        return instance