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
function convertTextToSign(text, outputContainerId, language = 'asl') {
    const words = text.toUpperCase().split(' ');
    const signOutput = document.getElementById(outputContainerId);
    const langFolder = language.toLowerCase() === 'isl' ? 'isl-images' : 'asl-images';

    if (!signOutput) return;

    // Clear previous output
    signOutput.innerHTML = '';

    // Process each word
    words.forEach((word, wordIndex) => {
        if (!word.trim()) return;

        const wordContainer = document.createElement('div');
        wordContainer.className = 'word-container';

        for (let i = 0; i < word.length; i++) {
            const char = word[i];

            if (/[A-Z0-9]/.test(char)) {
                const img = document.createElement('img');
                img.className = 'letter-image';
                img.src = `/static/${langFolder}/${char}.png`;
                img.alt = `${language.toUpperCase()} sign for ${char}`;
                img.title = char;

                const calculatedDelay = (wordIndex * 0.1) + (i * 0.05);
                img.style.animationDelay = `${Math.min(calculatedDelay, 1.5)}s`;

                img.onerror = function () {
                    const placeholder = document.createElement('div');
                    placeholder.className = 'letter-image missing';
                    placeholder.textContent = char;
                    placeholder.title = char;
                    placeholder.style.animationDelay = this.style.animationDelay;
                    this.parentNode.replaceChild(placeholder, this);
                };

                wordContainer.appendChild(img);
            }
        }

        if (wordContainer.children.length > 0) {
            signOutput.appendChild(wordContainer);
        }
    });

    if (signOutput.children.length > 0) {
        signOutput.parentElement.classList.remove('hidden');
        signOutput.parentElement.style.display = 'block';
        signOutput.scrollIntoView({ behavior: 'smooth', block: 'center' });
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
