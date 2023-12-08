function populateBuilding() {
    // Fetch the full list of places
    // First, fetch the place names
    const dropdown = document.getElementById('specific-building')
    const dynamicOptions = ['Option 1', 'Option 2', 'Option 3', 'Option 4'];

    // Clear the loading option
    dropdown.innerHTML = '';

    // Create and append options based on fetched data
    dynamicOptions.forEach(optionText => {
        const opt = document.createElement('option');
        opt.textContent = optionText;
        opt.value = optionText;
        dropdown.appendChild(opt);
    });
}

function populateClassroom() {
    // Fetch the full list of places

    // First, fetch the place names
    fetch('127.0.0.1:8000/all-classrooms')
        .then(response => response.json())
        .then(data => {
            var dropdown = document.getElementById("specific-building");

            // Now, iterate through
            data.forEach(item => {
                var option = document.createElement("option");
                option.text = option.value = item[0];
                dropdown.appendChild(option);
                console.log('hello')
            });
        })
        .catch(error => {
            console.error('Error fetching data:', error)
        });
}