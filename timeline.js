
function togglePopup(cardElement) {
    const popup = cardElement.querySelector('.hidden-popup');
    if (popup) {
      popup.style.display = popup.style.display === 'block' ? 'none' : 'block';
    }
  }
  
  
  document.addEventListener('DOMContentLoaded', () => {
    const fadeInElements = document.querySelectorAll('.fade-in');
  
    
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('show');
          observer.unobserve(entry.target); 
        }
      });
    }, {
      threshold: 0.1 
    });
  
    
    fadeInElements.forEach(el => {
      observer.observe(el);
    });
  });
  
