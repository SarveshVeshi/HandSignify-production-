/**
 * feature-utils.js
 * Shared utilities for UI toggles and Text-to-Sign conversion.
 */

/**
 * Sets up tab-based navigation for feature panels.
 * @param {string} buttonClass - Class name of tab buttons.
 * @param {string} contentClass - Class name of content panels.
 * @param {object} callbacks - Optional callbacks { onSwitch: function(targetId) }
 */
function setupFeatureToggle(buttonSelector = '.tab-button', contentSelector = '.tab-content', callbacks = {}) {
    const tabButtons = document.querySelectorAll(buttonSelector);

    tabButtons.forEach(button => {
        button.addEventListener('click', function () {
            const targetPanel = this.getAttribute('data-tab');

            // Update active states
            tabButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            // Show target panel, hide others
            document.querySelectorAll(contentSelector).forEach(panel => {
                panel.classList.remove('active');
            });
            document.getElementById(targetPanel).classList.add('active');

            // Invoke callback if provided
            if (callbacks.onSwitch) {
                callbacks.onSwitch(targetPanel);
            }
        });
    });
}

/**
 * Converts text input to sign images.
 * @param {string} text - Text to convert
 * @param {string} outputContainerId - ID of the container to append images to
 * @param {string} language - 'asl' or 'isl'
 */
async function convertTextToSign(text, outputContainerId, language = 'asl') {
    const signOutput = document.getElementById(outputContainerId);
    if (!signOutput) return;

    // Clear previous output
    signOutput.innerHTML = '<div class="loading-signs">Loading signs...</div>';

    try {
        const response = await fetch('/get_sign_images', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text, language }),
        });

        const data = await response.json();
        if (!data.success) {
            signOutput.innerHTML = '<div class="error-signs">Failed to load sign images.</div>';
            return;
        }

        // Clear loading state
        signOutput.innerHTML = '';

        const imagePaths = data.image_paths;
        if (imagePaths.length === 0) {
            signOutput.innerHTML = '<div class="info-signs">No signs found for the given text.</div>';
            return;
        }

        const wordContainer = document.createElement('div');
        wordContainer.className = 'word-container';

        imagePaths.forEach((path, index) => {
            const img = document.createElement('img');
            img.className = 'letter-image';
            img.src = `/static/${path}`;

            // Extract label (either word or letter) for alt/title
            const parts = path.split('/');
            const filename = parts[parts.length - 1];
            const label = filename.split('.')[1] || filename.split('.')[0];

            img.alt = `${language.toUpperCase()} sign for ${label}`;
            img.title = label;

            const calculatedDelay = index * 0.1;
            img.style.animationDelay = `${Math.min(calculatedDelay, 2.0)}s`;

            img.onerror = function () {
                const placeholder = document.createElement('div');
                placeholder.className = 'letter-image missing';
                placeholder.textContent = label.length > 1 ? '?' : label;
                placeholder.title = `Missing sign for ${label}`;
                placeholder.style.animationDelay = this.style.animationDelay;
                this.parentNode.replaceChild(placeholder, this);
            };

            wordContainer.appendChild(img);
        });

        signOutput.appendChild(wordContainer);

        if (signOutput.children.length > 0) {
            signOutput.parentElement.classList.remove('hidden');
            signOutput.parentElement.style.display = 'block';
            signOutput.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    } catch (error) {
        console.error('Error fetching sign images:', error);
        signOutput.innerHTML = '<div class="error-signs">Error connecting to server.</div>';
    }
}

/**
 * Shows an error message in a specified element.
 * @param {string} elementId - ID of the error element
 * @param {string} message - Error message text
 */
function showError(elementId, message) {
    const errorMessage = document.getElementById(elementId);
    if (errorMessage) {
        errorMessage.textContent = message;
        errorMessage.classList.remove('hidden');
    }
}
