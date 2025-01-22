// Reveal the hidden content inside a card
function togglePopup(cardElement) {
    const popup = cardElement.querySelector('.hidden-popup');
    if (popup) {
      popup.style.display = popup.style.display === 'block' ? 'none' : 'block';
    }
  }
  
  // On scroll, fade in timeline items using Intersection Observer
  document.addEventListener('DOMContentLoaded', () => {
    const fadeInElements = document.querySelectorAll('.fade-in');
  
    // Create the intersection observer
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('show');
          observer.unobserve(entry.target); // optional: stop observing once it's in view
        }
      });
    }, {
      threshold: 0.1 // adjust if you want it to trigger earlier/later
    });
  
    // Observe each fade-in element
    fadeInElements.forEach(el => {
      observer.observe(el);
    });
  });
  
