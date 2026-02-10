// Header scroll
const header = document.querySelector("header");

// Change header on scroll
window.addEventListener("scroll", () => {
  if (window.scrollY > 50) {
    header.classList.add("bg-light", "shadow-sm", "py-2");
    header.classList.remove("bg-transparent", "py-3");
  } else {
    header.classList.remove("bg-light", "shadow-sm", "py-2");
    header.classList.add("bg-transparent", "py-3");
  }
});// Portfolio Modal
const portfolioModal = document.getElementById('portfolio-modal');
const portfolioCarousel = document.getElementById('portfolio-carousel');
const lightboxCounter = document.getElementById('lightbox-counter');
const totalSlides = portfolioCarousel.querySelectorAll('.carousel-item').length;

if (portfolioModal) {
  portfolioModal.addEventListener('show.bs.modal', event => {
    const button = event.relatedTarget;
    const slideIndex = parseInt(button.closest('[data-bs-slide-to]').dataset.bsSlideTo);
    const carousel = new bootstrap.Carousel(portfolioCarousel);
    carousel.to(slideIndex);
    lightboxCounter.textContent = `${slideIndex + 1} / ${totalSlides}`;
  });

  portfolioCarousel.addEventListener('slid.bs.carousel', event => {
    const slideIndex = event.to;
    lightboxCounter.textContent = `${slideIndex + 1} / ${totalSlides}`;
  });
}

// Contact Form
const contactForm = document.getElementById("contact-form");
if(contactForm){
    contactForm.addEventListener("submit", (e) => {
        e.preventDefault();
        alert("Thank you for your message. We'll be in touch within 24 hours.");
        contactForm.reset();
    });
}

// Initialize jQuery UI Datepicker
// $(document).ready(function() {
//     console.log("Document ready, initializing datepicker.");
//     $("#datepicker-input").datepicker({
//         beforeShowDay: function(date) {
//             var day = date.getDay();
//             // Only allow Saturday (6) and Sunday (0)
//             return [(day == 6 || day == 0), ''];
//         },
//         showOtherMonths: true,
//         selectOtherMonths: true
//     });
// });

// Footer Year
// const yearEl = document.getElementById("year");
// if(yearEl) {
//     yearEl.textContent = new Date().getFullYear();
// }
// $(function () {
//   $("#datepicker-input").datepicker({
//     dateFormat: "yy-mm-dd",
//     minDate: 0,
//     beforeShowDay: function (date) {
//       const day = date.getDay();
//       // Allow only Saturday (6) and Sunday (0)
//       return [(day === 0 || day === 6)];
//     },
//   });
// });


// $(document).ready(function () {
//     $.getJSON("/api/unavailable-dates/", function (data) {
//         const unavailable = data.unavailable;

//         $("#datepicker-input").datepicker({
//             dateFormat: "yy-mm-dd",
//             minDate: 0,
//             beforeShowDay: function (date) {
//     const d = $.datepicker.formatDate("yy-mm-dd", date);
//     const day = date.getDay(); // 0 = Sunday, 6 = Saturday

//     // Block weekdays (Mon–Fri)
//     if (day !== 0 && day !== 6) {
//         return [false, "", "Weekdays not available"];
//     }

//     // Block unavailable dates from Google Calendar
//     if (unavailable.includes(d)) {
//         return [false, "booked", "Unavailable"];
//     }

//     // Allow only weekends
//     return [true, "", "Available"];
// }

//         });
//     });
// });


$(document).ready(function () {
    $.getJSON("/api/unavailable-dates/", function (data) {
        const unavailable = data.unavailable;

        $("#datepicker-input").datepicker({
            dateFormat: "yy-mm-dd",
            minDate: 0,
            beforeShowDay: function (date) {
                const d = $.datepicker.formatDate("yy-mm-dd", date);

                // Block unavailable dates from Google Calendar
                if (unavailable.includes(d)) {
                    return [false, "booked", "Unavailable"];
                }

                // Allow all days (Monday to Sunday)
                return [true, "", "Available"];
            }
        });
    });
});
