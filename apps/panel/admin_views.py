from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

def get_objects(request):
    # Get the content_type ID from the GET request parameters
    content_type_id = request.GET.get('content_type')

    # Initialize an empty list for serialized objects
    serialized_objects = []

    try:
        # Convert the ID to an integer and fetch the corresponding ContentType
        content_type = ContentType.objects.get_for_id(int(content_type_id))

        # Get the model class associated with this ContentType
        model = content_type.model_class()

        # Fetch all objects of this model (you may want to apply filters or order them)
        objects = model.objects.all()

        # Serialize the objects into a list of dictionaries
        serialized_objects = [{'id': obj.id, 'name': str(obj)} for obj in objects]
    except (ValueError, ObjectDoesNotExist):
        # If the content_type_id is not valid or no ContentType is found, handle the exception
        pass

    # Return the serialized objects as a JSON response
    return JsonResponse({'objects': serialized_objects})