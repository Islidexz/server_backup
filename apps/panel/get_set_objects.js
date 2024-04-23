document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('id_items_content_type').addEventListener('change', function() {
        var content_type = this.value;
        
        fetch(`/admin/get_set_objects/?content_type=${content_type}`)
            .then(response => response.json())
            .then(data => {
                var itemsDropdown = document.getElementById('id_items_object_id');
                itemsDropdown.innerHTML = '';
                
                data.objects.forEach(obj => {
                    var option = document.createElement('option');
                    option.value = obj.id;
                    option.text = obj.name;
                    itemsDropdown.appendChild(option);
                });
            })
            .catch(error => console.error('Error:', error));
    });
});