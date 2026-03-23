(function () {
    window.trackit = function () {};

    var state = {
        isDragging: false,
        isAnimating: false,
        cueball: null,
        line: null,
        initX: 0,
        initY: 0,
        scale: 4
    };

    function updateStatus(text) {
        var el = document.getElementById('game-status');
        if (el) el.textContent = text;
    }

    function sendVelocity(vx, vy) {
        if (state.isAnimating) return;
        updateStatus('Simulating shot\u2026');

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/handle_mouse_position', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    handleSVGResponse(xhr.responseText);
                } else {
                    updateStatus('Server error \u2014 try again');
                }
            }
        };
        xhr.send(JSON.stringify({ vx: vx, vy: vy }));
    }

    function stripSVGPreamble(s) {
        var idx = s.indexOf('<svg');
        return idx >= 0 ? s.substring(idx) : s;
    }

    function highlightPlayer(playerName) {
        var badges = document.querySelectorAll('.player-badge');
        for (var i = 0; i < badges.length; i++) {
            if (playerName && badges[i].getAttribute('data-player') === playerName) {
                badges[i].classList.add('active');
            } else {
                badges[i].classList.remove('active');
            }
        }
    }

    function handleSVGResponse(responseText) {
        if (!responseText || responseText.trim() === '') return;

        try {
            var response = JSON.parse(responseText);
            var svgs = response.svgs;
            var currentPlayer = response.current_player;
            var winner = response.winner || null;

            if (!svgs || svgs.length === 0) return;

            var cleaned = [];
            for (var i = 0; i < svgs.length; i++) {
                cleaned.push(stripSVGPreamble(svgs[i]));
            }
            animateFrames(cleaned, currentPlayer, winner);
        } catch (e) {
            console.error('Failed to parse SVG response:', e);
            updateStatus('Error displaying shot');
        }
    }

    function animateFrames(svgs, currentPlayer, winner) {
        state.isAnimating = true;
        updateStatus('Shot in progress\u2026');

        var container = document.getElementById('svg-container');
        var totalFrames = svgs.length;

        var targetFPS = 30;
        var frameDelay = Math.round(1000 / targetFPS);
        var maxAnimSeconds = 8;
        var maxFramesToShow = maxAnimSeconds * targetFPS;
        var skipFactor = Math.max(1, Math.ceil(totalFrames / maxFramesToShow));

        var displayFrames = [];
        for (var i = 0; i < totalFrames; i += skipFactor) {
            displayFrames.push(svgs[i]);
        }
        if (displayFrames[displayFrames.length - 1] !== svgs[totalFrames - 1]) {
            displayFrames.push(svgs[totalFrames - 1]);
        }

        var idx = 0;

        function tick() {
            if (idx >= displayFrames.length) {
                state.isAnimating = false;

                if (winner) {
                    var statusEl = document.getElementById('game-status');
                    statusEl.textContent = winner + ' wins!';
                    statusEl.classList.add('game-over');
                    highlightPlayer(winner);
                } else {
                    updateStatus('Drag the cue ball to shoot');
                    highlightPlayer(currentPlayer);
                    setupCueBallInteraction();
                }
                return;
            }
            container.innerHTML = displayFrames[idx];
            idx++;
            setTimeout(tick, frameDelay);
        }

        tick();
    }

    function setupCueBallInteraction() {
        var container = document.getElementById('svg-container');
        if (!container) return;

        var cueball = container.querySelector('circle[fill="WHITE"]');
        if (!cueball) {
            updateStatus('Cue ball is off the table');
            return;
        }

        var svg = container.querySelector('svg');
        if (!svg) return;

        var oldLine = svg.querySelector('#aim-line');
        if (oldLine) oldLine.remove();

        var line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('id', 'aim-line');
        line.setAttribute('stroke', 'rgba(255,255,255,0.7)');
        line.setAttribute('stroke-width', '6');
        line.setAttribute('stroke-dasharray', '20,12');
        line.setAttribute('stroke-linecap', 'round');
        line.style.display = 'none';
        svg.appendChild(line);
        state.line = line;

        var fresh = cueball.cloneNode(true);
        cueball.parentNode.replaceChild(fresh, cueball);
        state.cueball = fresh;
        fresh.style.cursor = 'grab';

        fresh.addEventListener('mousedown', function (e) {
            if (state.isAnimating) return;
            e.preventDefault();
            state.isDragging = true;
            fresh.style.cursor = 'grabbing';
            state.initX = e.clientX;
            state.initY = e.clientY;

            var cx = fresh.cx.baseVal.value;
            var cy = fresh.cy.baseVal.value;
            line.style.display = 'block';
            line.setAttribute('x1', cx);
            line.setAttribute('y1', cy);
            line.setAttribute('x2', cx);
            line.setAttribute('y2', cy);
        });
    }

    document.addEventListener('mousemove', function (e) {
        if (!state.isDragging || !state.cueball || !state.line) return;

        var cx = parseFloat(state.cueball.getAttribute('cx'));
        var cy = parseFloat(state.cueball.getAttribute('cy'));
        var adjustedX = (e.clientX - state.initX) * state.scale + cx;
        var adjustedY = (e.clientY - state.initY) * state.scale + cy;

        state.line.setAttribute('x2', adjustedX);
        state.line.setAttribute('y2', adjustedY);
    });

    document.addEventListener('mouseup', function (e) {
        if (!state.isDragging || !state.cueball) return;
        state.isDragging = false;

        if (state.cueball) state.cueball.style.cursor = 'grab';
        if (state.line) state.line.style.display = 'none';

        var cx = parseFloat(state.cueball.getAttribute('cx'));
        var cy = parseFloat(state.cueball.getAttribute('cy'));
        var adjustedX = (e.clientX - state.initX) * state.scale + cx;
        var adjustedY = (e.clientY - state.initY) * state.scale + cy;

        var finalX = adjustedX - cx;
        var finalY = adjustedY - cy;
        var velocityX = -(finalX * state.scale);
        var velocityY = -(finalY * state.scale);

        if (Math.abs(velocityX) < 5 && Math.abs(velocityY) < 5) return;

        sendVelocity(velocityX, velocityY);
    });

    document.addEventListener('DOMContentLoaded', function () {
        var svgContainer = document.getElementById('svg-container');
        if (!svgContainer) return;

        var defaultSVG =
            '<svg width="700" height="1375" viewBox="-25 -25 1400 2750" ' +
            'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">' +
            '<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />' +
            '<rect width="1400" height="25" x="-25" y="-25" fill="darkgreen" />' +
            '<rect width="1400" height="25" x="-25" y="2700" fill="darkgreen" />' +
            '<rect width="25" height="2750" x="-25" y="-25" fill="darkgreen" />' +
            '<rect width="25" height="2750" x="1350" y="-25" fill="darkgreen" />' +
            '<circle cx="0" cy="0" r="114" fill="black" />' +
            '<circle cx="0" cy="1350" r="114" fill="black" />' +
            '<circle cx="0" cy="2700" r="114" fill="black" />' +
            '<circle cx="1350" cy="0" r="114" fill="black" />' +
            '<circle cx="1350" cy="1350" r="114" fill="black" />' +
            '<circle cx="1350" cy="2700" r="114" fill="black" />' +
            '<circle cx="675" cy="2025" r="28.5" fill="WHITE" />' +
            '<circle cx="675" cy="675" r="28.5" fill="YELLOW" />' +
            '<circle cx="615" cy="630" r="28.5" fill="BLUE" />' +
            '<circle cx="735" cy="630" r="28.5" fill="RED" />' +
            '<circle cx="555" cy="585" r="28.5" fill="PURPLE" />' +
            '<circle cx="675" cy="585" r="28.5" fill="ORANGE" />' +
            '<circle cx="795" cy="585" r="28.5" fill="GREEN" />' +
            '<circle cx="495" cy="540" r="28.5" fill="BROWN" />' +
            '<circle cx="615" cy="540" r="28.5" fill="BLACK" />' +
            '<circle cx="735" cy="540" r="28.5" fill="LIGHTYELLOW" />' +
            '<circle cx="855" cy="540" r="28.5" fill="LIGHTBLUE" />' +
            '</svg>';

        svgContainer.innerHTML = defaultSVG;
        setupCueBallInteraction();
    });
})();
