/**
 * Miracle Flowers — forms.js
 * Lightweight client-side validation feedback for the contact form.
 * Server-side validation (Django forms) always remains the source of
 * truth; this only improves the interactive experience.
 */
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    var form = document.querySelector("[data-contact-form]");
    if (!form) return;

    var submitBtn = form.querySelector('button[type="submit"]');

    form.addEventListener("submit", function (event) {
      var valid = true;

      form.querySelectorAll("[data-required]").forEach(function (field) {
        var wrapper = field.closest(".form-field");
        var value = field.value.trim();
        if (!value) {
          valid = false;
          wrapper && wrapper.classList.add("has-error");
        } else {
          wrapper && wrapper.classList.remove("has-error");
        }
      });

      var emailField = form.querySelector('[name="email"]');
      if (emailField && emailField.value.trim()) {
        var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        var wrapper = emailField.closest(".form-field");
        if (!emailPattern.test(emailField.value.trim())) {
          valid = false;
          wrapper && wrapper.classList.add("has-error");
        }
      }

      if (!valid) {
        event.preventDefault();
        return;
      }

      if (submitBtn) {
        submitBtn.setAttribute("aria-disabled", "true");
        form.classList.add("form-submitting");
        submitBtn.textContent = "Sending...";
      }
    });

    // Clear the error state as soon as the visitor starts fixing a field.
    form.querySelectorAll("input, textarea").forEach(function (field) {
      field.addEventListener("input", function () {
        var wrapper = field.closest(".form-field");
        wrapper && wrapper.classList.remove("has-error");
      });
    });
  });
})();
