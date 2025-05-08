// Timer functionality
document.addEventListener('DOMContentLoaded', function() {
    // Constants
    const TIMER_DURATION = 10 * 60 * 1000; // 10 minutes in milliseconds
    
    // Elements
    const timerContainer = document.getElementById('timer-container');
    const timerCountdown = document.getElementById('timer-countdown');
    
    // If we're on the start page, don't initialize the timer
    if (window.location.pathname === '/' || !timerContainer) {
        return;
    }
    
    // Check if timer already exists in localStorage
    let timerStartTime = localStorage.getItem('timerStartTime');
    
    // If timer doesn't exist, create it
    if (!timerStartTime) {
        timerStartTime = Date.now();
        localStorage.setItem('timerStartTime', timerStartTime);
    }
    
    // Update timer function
    function updateTimer() {
        const currentTime = Date.now();
        const elapsedTime = currentTime - parseInt(timerStartTime);
        const remainingTime = TIMER_DURATION - elapsedTime;
        
        // If time is up, redirect to the landing page
        if (remainingTime <= 0) {
            localStorage.removeItem('timerStartTime');
            alert('Time is up! You will be redirected to the start page.');
            window.location.href = '/';
            return;
        }
        
        // Calculate minutes and seconds
        const minutes = Math.floor(remainingTime / 60000);
        const seconds = Math.floor((remainingTime % 60000) / 1000);
        
        // Display the time
        timerCountdown.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        // Add warning class when less than 2 minutes remaining
        if (remainingTime < 120000) {
            timerCountdown.classList.add('warning');
        } else {
            timerCountdown.classList.remove('warning');
        }
    }
    
    // Initial update
    updateTimer();
    
    // Update timer every second
    const timerInterval = setInterval(updateTimer, 1000);
    
    // Clean up on page unload
    window.addEventListener('beforeunload', function() {
        clearInterval(timerInterval);
    });
});