document.addEventListener('DOMContentLoaded', () => {
    const tableContainer = document.getElementById('table-container');

    fetch('http://127.0.0.1:5000/api/venues')
        .then(response => {
            if (!response.ok) throw new Error(`Backend error: ${response.status}`);
            return response.json();
        })
        .then(data => {
            if (!data || data.length === 0) {
                tableContainer.innerHTML = '<p class="text-gray-500">No venues found.</p>';
                return;
            }

            const table = document.createElement('table');
            table.className = 'min-w-full bg-white border-collapse';
            const thead = document.createElement('thead');
            thead.className = 'bg-gray-800 text-white';
            const tbody = document.createElement('tbody');
            tbody.className = 'text-gray-700';

            // Custom columns in desired order
            const columns = [
                { key: 'name', label: 'Venue' },
                { key: 'address', label: 'Address' },
                { key: 'category', label: 'Category' },
                { key: 'phone_number', label: 'Phone Number' },
                { key: 'rating', label: 'Rating' },
                { key: 'x_coordinate', label: 'X Coordinate' },
                { key: 'y_coordinate', label: 'Y Coordinate' },
                { key: 'website_url', label: 'website' },
                { key: 'instagram', label: 'Instagram' },
                { key: 'facebook', label: 'Facebook' },
            ];

            const headerRow = document.createElement('tr');
            columns.forEach(column => {
                const th = document.createElement('th');
                th.className = 'py-2 px-4 border';
                th.textContent = column.label;
                headerRow.appendChild(th);
            });
            thead.appendChild(headerRow);
            table.appendChild(thead);

            // Rows
            data.forEach(venue => {
                const row = document.createElement('tr');
                row.className = 'border-b';
                columns.forEach(column => {
                    const td = document.createElement('td');
                    td.className = 'py-2 px-4 border';
                    let value = venue[column.key];

                    // Format date columns
                    if (column.key === 'upcoming_event_date' && value) {
                        const date = new Date(value);
                        value = !isNaN(date) ? date.toLocaleString() : 'Invalid Date';
                    }
                    // Handle boolean flags (if any)
                    else if (typeof value === 'boolean') {
                        value = value ? 'Yes' : 'No';
                    }

                    td.textContent = value !== null && value !== undefined ? value : 'N/A';
                    row.appendChild(td);
                });
                tbody.appendChild(row);
            });
            table.appendChild(tbody);
            tableContainer.appendChild(table);
        })
        .catch(error => {
            console.error('Error:', error);
            tableContainer.innerHTML = '<p class="text-red-500">Error: Check backend at http://127.0.0.1:5000. Details: ' + error.message + '</p>';
        });
});