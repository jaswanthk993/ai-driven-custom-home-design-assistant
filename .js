document.addEventListener('DOMContentLoaded', function() {
    // Update range input values
    const ranges = ['bedrooms', 'bathrooms', 'additionalRooms', 'houseSize'];
    ranges.forEach(id => {
        const input = document.getElementById(id);
        const value = document.getElementById(`${id}Value`);
        input.addEventListener('input', () => value.textContent = input.value);
    });

    // Handle form submission
    document.getElementById('designForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        const generateBtn = document.getElementById('generateBtn');
        generateBtn.disabled = true;
        generateBtn.textContent = 'Generating...';

        try {
            // Gather form data
            const requirements = Array.from(document.querySelectorAll('input[type="checkbox"]:checked'))
                .map(cb => cb.value);

            const formData = {
                num_bedrooms: parseInt(document.getElementById('bedrooms').value),
                num_bathrooms: parseInt(document.getElementById('bathrooms').value),
                additional_rooms: parseInt(document.getElementById('additionalRooms').value),
                house_size: parseInt(document.getElementById('houseSize').value),
                style: document.getElementById('style').value,
                requirements: requirements,
                num_rooms: parseInt(document.getElementById('bedrooms').value) +
                          parseInt(document.getElementById('bathrooms').value) +
                          parseInt(document.getElementById('additionalRooms').value) + 2
            };

            // Send request to generate design
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();
            
            if (!data.success) {
                throw new Error(data.error);
            }

            // Create floor plan visualization
            createFloorPlan(data.layout);
            
            // Show design details
            updateDesignDetails(formData);
            
            // Show export buttons
            document.getElementById('exportButtons').style.display = 'flex';
            
            // Setup export buttons
            setupExportButtons(data.layout, formData);

        } catch (error) {
            alert('Error generating design: ' + error.message);
        } finally {
            generateBtn.disabled = false;
            generateBtn.textContent = 'Generate Design';
        }
    });

    function createFloorPlan(layoutData) {
        const colorMap = {
            'bedroom': '#B3E5FC',
            'bathroom': '#F5F5F5',
            'kitchen': '#FFECB3',
            'living_room': '#C8E6C9',
            'dining_room': '#FFE0B2',
            'office': '#E1BEE7'
        };

        const shapes = layoutData.map(room => ({
            type: 'rect',
            x0: room.x,
            y0: room.y,
            x1: room.x + room.width,
            y1: room.y + room.height,
            line: { color: 'black', width: 2 },
            fillcolor: colorMap[room.room_type] || '#FFFFFF'
        }));

        const annotations = layoutData.map(room => ({
            x: room.x + room.width/2,
            y: room.y + room.height/2,
            text: `${room.room_type}<br>(${Math.round(room.size)} sq ft)`,
            showarrow: false,
            font: { size: 12 },
            bgcolor: 'rgba(255, 255, 255, 0.8)'
        }));

        const layout = {
            showlegend: false,
            plot_bgcolor: 'white',
            width: 800,
            height: 600,
            margin: { l: 20, r: 20, t: 20, b: 20 },
            xaxis: {
                showgrid: false,
                zeroline: false,
                showticklabels: false
            },
            yaxis: {
                showgrid: false,
                zeroline: false,
                showticklabels: false,
                scaleanchor: 'x',
                scaleratio: 1
            },
            shapes: shapes,
            annotations: annotations
        };

        Plotly.newPlot('floorPlan', [], layout);
    }

    function updateDesignDetails(formData) {
        const details = document.getElementById('designDetails');
        details.innerHTML = `
            <div class="metric">
                <h3>Total Area</h3>
                <p>${formData.house_size} sq ft</p>
            </div>
            <div class="metric">
                <h3>Bedrooms</h3>
                <p>${formData.num_bedrooms}</p>
            </div>
            <div class="metric">
                <h3>Total Rooms</h3>
                <p>${formData.num_rooms}</p>
            </div>
        `;
    }

    function setupExportButtons(layoutData, formData) {
        // JSON Export
        document.getElementById('downloadJSON').onclick = () => {
            const summary = {
                project_info: {
                    total_area: formData.house_size,
                    style: formData.style,
                    special_requirements: formData.requirements
                },
                rooms: layoutData
            };
            
            downloadFile(
                JSON.stringify(summary, null, 2),
                'floor_plan_summary.json',
                'application/json'
            );
        };

        // CSV Export
        document.getElementById('downloadCSV').onclick = () => {
            const headers = Object.keys(layoutData[0]);
            const csv = [
                headers.join(','),
                ...layoutData.map(row => headers.map(field => row[field]).join(','))
            ].join('\n');
            
            downloadFile(csv, 'floor_plan_data.csv', 'text/csv');
        };
    }

    function downloadFile(content, filename, type) {
        const blob = new Blob([content], { type });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        window.URL.revokeObjectURL(url);
    }
});
