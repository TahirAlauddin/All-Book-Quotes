// Wait for the document to be ready
document.addEventListener("DOMContentLoaded", function(event) { 

    // Add click animation to elements with the "clickable" class
    let clickableElements = document.querySelectorAll(".clickable");
    clickableElements.forEach(element => {
      element.addEventListener("click", function() {
        element.classList.add("animate__animated", "animate__bounce");
        // Remove animation classes after animation completes
        setTimeout(() => {
          element.classList.remove("animate__animated", "animate__bounce");
        }, 1000);
      });
    });
  
    // Add animation to elements with the "slide-in" class when they come into view
    let slideInElements = document.querySelectorAll(".slide-in");
    slideInElements.forEach(element => {
      let options = {
        threshold: 0.5 // Trigger animation when element is 50% in view
      };
      let observer = new IntersectionObserver(function(entries, observer) {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            element.classList.add("animate__animated", "animate__slideInLeft");
            // Unobserve element after animation completes
            observer.unobserve(entry.target);
          }
        });
      }, options);
      observer.observe(element);
    });
  
  });
  