document.addEventListener('DOMContentLoaded', function() {
    var itemsContentTypeSelect = document.getElementById('id_items_content_type');
    var itemsDropdown = document.getElementById('id_items_object_id');

    if (!itemsContentTypeSelect) {
        console.error('Element with ID "id_items_content_type" was not found.');
        return; // Stop the function if the element is not found
    }

    if (!itemsDropdown) {
        console.error('Element with ID "id_items_object_id" was not found.');
        return; // Stop the function if the element is not found
    }

    // Add an event listener for when the selected option in 'itemsContentTypeSelect' changes
    itemsContentTypeSelect.addEventListener('change', function() {
        var content_type = this.value;
        
        // Make sure to handle empty values if no option is selected
        if (!content_type) {
            itemsDropdown.innerHTML = '<option value="">---------</option>';
            return;
        }
        
        fetch(`get_set_objects/?content_type=${content_type}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                itemsDropdown.innerHTML = '';
                data.objects.forEach(obj => {
                    var option = document.createElement('option');
                    option.value = obj.id;
                    option.text = obj.name;
                    itemsDropdown.appendChild(option);
                });
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Failed to fetch data: ' + error.message);
            });
    });
});