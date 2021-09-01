

class RecipeStepDraftBulkCreateSerializer(serializers.ListSerializer):
    
    def validate(self, data):
        print("bulk validate")
        new_step_numbers = [s.get('step_number') for s in data]
        if None in new_step_numbers:
            raise serializers.ValidationError("step_number filed is required")
        if new_step_numbers != list(set(new_step_numbers)):
            raise serializers.ValidationError("Wrong order of step_number(s) supplied")
        try:
            recipe = Recipe.objects.get(pk=self.context.get('recipe_id'))
            existing_steps = recipe.recipe_steps.get_queryset().all()
            if existing_steps:
                ex_step_numbers = [s.step_number for s in existing_steps]
                if new_step_numbers[0] != ex_step_numbers[-1] + 1:
                   raise serializers.ValidationError(
                    f"The next first supplied step_number must be: {ex_step_numbers[-1] + 1}") 
                steps_combined = ex_step_numbers + new_step_numbers
                if steps_combined != list(set(steps_combined)): 
                    raise serializers.ValidationError(f"Wrong order of step_number(s) supplied")  
            return data   
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Recipe under provided id doesn't exist.")    
    def create(self, validated_data):
        recipe = Recipe.objects.get(pk=self.context.get('recipe_id'))
        for step in validated_data:
            step['recipe'] = recipe
            RecipeStep.objects.create(**step)
        return validated_data                

class RecipeStepDraftCreateSerializer(serializers.ModelSerializer):  

    class Meta:
        model = RecipeStep 
        fields = [ 
            'id',
            'step_number',
            'step_image',
            'instruction',
            'tip']  
        list_serializer_class = RecipeStepDraftBulkCreateSerializer
    
    def validate(self, data):
        print("single validate")
        if not data.get("step_number"):
            raise serializers.ValidationError("step_number field is required.")
        try:
            recipe = Recipe.objects.get(pk=self.context.get('recipe_id'))
            existing_steps = recipe.recipe_steps.get_queryset().all()
            if existing_steps:
                ex_step_numbers = [s.step_number for s in existing_steps]
                if data["step_number"] != ex_step_numbers[-1] + 1:
                    raise serializers.ValidationError(
                    f"The next first supplied step_number must be: {ex_step_numbers[-1] + 1}") 
            if data["step_number"] != 1:
            	raise serializers.ValidationError(f"Wrong step_number. 1 expected, got {data['step_number']}")        
            return data
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Recipe under provided id doesn't exist.")
                      

    def create(self, validated_data):
        recipe = Recipe.objects.get(pk=self.context.get('recipe_id'))
        validated_data['recipe'] = recipe
        step = RecipeStep.objects.create(**validated_data)
        return step 