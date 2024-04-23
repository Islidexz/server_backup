
// JavaScript to close the dropdown when clicking outside of it or pressing the escape key
document.addEventListener('DOMContentLoaded', function() {
        var elems = document.querySelectorAll('.dropdown-trigger');
        var options = {
            // Specify options here if needed
        };
        var instances = M.Dropdown.init(elems, options);


    // Attach click events to each trigger
    dropdowns.forEach(function(trigger) {
        trigger.addEventListener('click', function(event) {
            var targetId = trigger.getAttribute('data-target');
            var dropdown = document.getElementById(targetId);

            // Hide any other open dropdowns
            openDropdowns().forEach(function(openDropdown) {
                if(openDropdown.id !== targetId) {
                    openDropdown.classList.remove('is-visible');
                }
            });

            // Toggle the visibility of the dropdown
            dropdown.classList.toggle('is-visible');
            
            event.preventDefault(); // Prevent default link behavior
        });
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', function(event) {
        if (!event.target.matches('.dropdown-trigger')) {
            openDropdowns().forEach(function(openDropdown) {
                openDropdown.classList.remove('is-visible');
            });
        }
    });

    // Close dropdowns when pressing the escape key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            openDropdowns().forEach(function(openDropdown) {
                openDropdown.classList.remove('is-visible');
            });
        }
    });
});
