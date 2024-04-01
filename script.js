// Function to send velocity to the server
    // Function to send velocity data and fetch SVGs from the server
    function sendVelocity(vx, vy) {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/handle_mouse_position", true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                console.log("DONE\n\n");
                if (xhr.status === 200) {
                    console.log("Mouse position sent successfully!");
                    handleSVGResponse(xhr.responseText); // Handle SVG response
                } else {
                    console.error("Error fetching SVGs from the server. Status code:", xhr.status);
                }
            }
        };
        var data = JSON.stringify({ "vx": vx, "vy": vy });
        xhr.send(data);
    }
    


    // Function to handle SVG response
    function handleSVGResponse(responseText) {
        console.log("Response received:", responseText); // Log the responseText for debugging
        var svgContainer = document.getElementById('svg-container');
        svgContainer.innerHTML = ''; // Clear previous content
    
        if (responseText.trim() === "") {
            console.error("Empty response received"); // Log an error if the response is empty
            return; // Exit the function early if the response is empty
        }
    
        try {
            var svgs = JSON.parse(responseText);
            svgs.forEach(function(svgData) {
                var objectTag = document.createElement('object');
                objectTag.setAttribute('type', 'image/svg+xml');
                objectTag.setAttribute('data', 'data:image/svg+xml,' + encodeURIComponent(svgData));
                svgContainer.appendChild(objectTag);
            });
        } catch (error) {
            console.error("Error parsing JSON:", error); // Log any errors that occur during JSON parsing
        }
    }
    

    document.addEventListener('DOMContentLoaded', function () {
        // Create the default SVG element
        var defaultSVG = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>' +
            '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">' +
            '<svg width="700" height="1375" viewBox="-25 -25 1400 2750" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">' +
            '<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" /> <rect width="1400" height="25" x="-25" y="-25" fill="darkgreen" />' +
            '<rect width="1400" height="25" x="-25" y="2700" fill="darkgreen" />' +
            '<rect width="25" height="2750" x="-25" y="-25" fill="darkgreen" />' +
            '<rect width="25" height="2750" x="1350" y="-25" fill="darkgreen" />' +
            '<circle cx="0.0" cy="0.0" r="114.0" fill="black" />' +
            '<circle cx="0.0" cy="1350.0" r="114.0" fill="black" />' +
            '<circle cx="0.0" cy="2700.0" r="114.0" fill="black" />' +
            '<circle cx="1350.0" cy="0.0" r="114.0" fill="black" />' +
            '<circle cx="1350.0" cy="1350.0" r="114.0" fill="black" />' +
            '<circle cx="1350.0" cy="2700.0" r="114.0" fill="black" />' +
            '<circle id="cueball" cx="675.0" cy="2025.0" r="28.5" fill="WHITE" />' +
            '<circle cx="675.0" cy="675.0" r="28.5" fill="YELLOW" />' +
            '<circle cx="615.0" cy="630.0" r="28.5" fill="BLUE" />' +
            '<circle cx="735.0" cy="630.0" r="28.5" fill="RED" />' +
            '<circle cx="555.0" cy="585.0" r="28.5" fill="PURPLE" />' +
            '<circle cx="675.0" cy="585.0" r="28.5" fill="ORANGE" />' +
            '<circle cx="795.0" cy="585.0" r="28.5" fill="GREEN" />' +
            '<circle cx="495.0" cy="540.0" r="28.5" fill="BROWN" />' +
            '<circle cx="615.0" cy="540.0" r="28.5" fill="BLACK" />' +
            '<circle cx="735.0" cy="540.0" r="28.5" fill="LIGHTYELLOW" />' +
            '<circle cx="855.0" cy="540.0" r="28.5" fill="LIGHTBLUE" />' +
            '</svg>';

        // Append the default SVG to the container
        var svgContainer = document.getElementById('svg-container');
        svgContainer.innerHTML = defaultSVG;

        // Get the cueball element from the SVG
        var cueball = svgContainer.querySelector('circle[fill="WHITE"]');
        var line = document.createElementNS("http://www.w3.org/2000/svg", "line");
        line.setAttribute('id', 'line');
        line.setAttribute('stroke', 'black');
        line.setAttribute('stroke-width', '10');
        cueball.parentNode.appendChild(line);

        // Define constants for scaling
        var scale = 4; // Adjust as needed

        // Variables to track mouse coordinates and dragging state
        var isDragging = false;
        var initX, initY; // Define initX and initY outside of the event listeners

        // Variables to store initial position for velocity calculation
        var initialCueballX, initialCueballY;

        // Function to handle mousedown event on the cueball
        function onMouseDown(event) {
            isDragging = true;

            initX = event.clientX; // Assign value to initX
            initY = event.clientY; // Assign value to initY

            initialCueballX = cueball.cx.baseVal.value;
            initialCueballY = cueball.cy.baseVal.value;

            // Show the line
            line.style.display = 'block';

            // Set line starting point to cueball position
            line.setAttribute('x1', cueball.cx.baseVal.value);
            line.setAttribute('y1', cueball.cy.baseVal.value);

            // Set line ending point to cueball position initially
            line.setAttribute('x2', cueball.cx.baseVal.value);
            line.setAttribute('y2', cueball.cy.baseVal.value);
        }

        // Function to handle mousemove event
        function onMouseMove(event) {
            if (isDragging) {
                var adjustedX = (event.clientX - initX) * scale + parseFloat(cueball.getAttribute('cx'));
                var adjustedY = (event.clientY - initY) * scale + parseFloat(cueball.getAttribute('cy'));
                // Update the line position to end at the adjusted mouse position
                line.setAttribute('x2', adjustedX);
                line.setAttribute('y2', adjustedY);
            }
        }

        // Function to handle mouseup event
        function onMouseUp(event) {
            isDragging = false;

            var adjustedX = (event.clientX - initX) * scale + parseFloat(cueball.getAttribute('cx'));
            var adjustedY = (event.clientY - initY) * scale + parseFloat(cueball.getAttribute('cy'));

            var finalX = (adjustedX - parseFloat(cueball.getAttribute('cx')));
            var finalY = (adjustedY - parseFloat(cueball.getAttribute('cy')));

            console.log(finalX);
            console.log(finalY);
            // Hide the line when dragging stops
            line.style.display = 'none';

            // Calculate velocity
            var velocityX = -(finalX * scale);
            var velocityY = -(finalY * scale);    

            console.log("Velocity X:", velocityX);
            console.log("Velocity Y:", velocityY);

            // Send finalX and finalY to the server
            sendVelocity(velocityX, velocityY);
        }

        // Add mousedown event listener to the cueball
        cueball.addEventListener('mousedown', onMouseDown);
        // Add mousemove event listener to the document
        document.addEventListener('mousemove', onMouseMove);

        // Add mouseup event listener to the document
        document.addEventListener('mouseup', onMouseUp);
    });
