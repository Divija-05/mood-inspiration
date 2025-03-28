document.addEventListener('DOMContentLoaded', function() {
    // Navigation between sections
    const startBtn = document.getElementById('start-btn');
    const nameForm = document.getElementById('name-form');
    const welcomeSection = document.getElementById('welcome-section');
    const nameSection = document.getElementById('name-section');
    const questionnaireSection = document.getElementById('questionnaire-section');
    const nameInput = document.getElementById('name-input');
    const nameHidden = document.getElementById('name-hidden');

    // Add smooth transition class to all sections
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.classList.add('transition-fade');
    });

    // Start button click
    if (startBtn) {
        startBtn.addEventListener('click', function() {
            animateTransition(welcomeSection, nameSection);
        });
    }

    // Name form submission
    if (nameForm) {
        nameForm.addEventListener('submit', function(e) {
            e.preventDefault();
            nameHidden.value = nameInput.value;
            animateTransition(nameSection, questionnaireSection);
        });
    }

    // Function to handle smooth transitions between sections
    function animateTransition(fromSection, toSection) {
        // Start exit animation
        fromSection.classList.add('is-exiting');
        
        // After exit animation completes, hide current section and show next
        setTimeout(() => {
            fromSection.classList.remove('active', 'is-exiting');
            toSection.classList.add('active');
            
            // Add entrance animation class
            toSection.classList.add('is-entering');
            
            // Remove entrance animation class after animation completes
            setTimeout(() => {
                toSection.classList.remove('is-entering');
            }, 500);
        }, 500);
    }

    // Rating selection animation
    const ratingLabels = document.querySelectorAll('.rating label');
    ratingLabels.forEach(label => {
        label.addEventListener('click', function() {
            // Add pulse animation
            this.classList.add('pulse-animation');
            
            // Remove animation class after it completes
            setTimeout(() => {
                this.classList.remove('pulse-animation');
            }, 500);
        });
    });
});
