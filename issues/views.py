class DraftsRecipeStepsCreateView(APIView):
	
	serializer_class = RecipeStepDraftCreateSerializer	

	def post(self, request, *args, **kwargs):

		print(f'DATA IS LIST: {isinstance(request.data, list)}')
		
		serializer = self.serializer_class(
			data=request.data, 
			many=isinstance(request.data, list), 
			context={
				'request': request,
				'recipe_id': kwargs.get('recipe_id')})
		serializer.is_valid(raise_exception=True)
		serializer.save()	
		return Response(serializer.data, status=status.HTTP_201_CREATED)