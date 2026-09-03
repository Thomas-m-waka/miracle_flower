/**
 * Miracle Flowers — main.js
 * Mobile navigation, scroll-based navbar effect, smooth scroll for
 * in-page anchors. Vanilla JavaScript only, no external dependencies.
 */
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    initMobileNav();
    initScrollNavbar();
    initSmoothScroll();
  });

  function initMobileNav() {
    var toggle = document.querySelector(".navbar__toggle");
    var panel = document.querySelector(".navbar__mobile-panel");
    if (!toggle || !panel) return;

    toggle.addEventListener("click", function () {
      var isOpen = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!isOpen));
      panel.classList.toggle("is-open", !isOpen);
    });

    // Close the mobile menu when a link inside it is clicked.
    panel.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        toggle.setAttribute("aria-expanded", "false");
        panel.classList.remove("is-open");
      });
    });
  }

  function initScrollNavbar() {
    var header = document.querySelector(".site-header");
    if (!header) return;

    var onScroll = function () {
      header.classList.toggle("is-scrolled", window.scrollY > 12);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(function (link) {
      link.addEventListener("click", function (event) {
        var targetId = link.getAttribute("href");
        if (!targetId || targetId === "#") return;
        var target = document.querySelector(targetId);
        if (!target) return;
        event.preventDefault();
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    });
  }
})();
