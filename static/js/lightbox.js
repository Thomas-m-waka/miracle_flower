/**
 * Miracle Flowers — lightbox.js
 * A lightweight, dependency-free image lightbox for gallery pages.
 * Works on any collection of `[data-lightbox-item]` elements that wrap
 * an <img> and share the same `data-lightbox-group`.
 */
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    var items = Array.prototype.slice.call(
      document.querySelectorAll("[data-lightbox-item]")
    );
    if (!items.length) return;

    var lightbox = buildLightbox();
    document.body.appendChild(lightbox.root);

    var currentIndex = 0;

    items.forEach(function (item, index) {
      item.addEventListener("click", function (event) {
        event.preventDefault();
        currentIndex = index;
        openLightbox(currentIndex);
      });
    });

    lightbox.closeBtn.addEventListener("click", closeLightbox);
    lightbox.prevBtn.addEventListener("click", function () {
      step(-1);
    });
    lightbox.nextBtn.addEventListener("click", function () {
      step(1);
    });
    lightbox.root.addEventListener("click", function (event) {
      if (event.target === lightbox.root) closeLightbox();
    });
    document.addEventListener("keydown", function (event) {
      if (!lightbox.root.classList.contains("is-open")) return;
      if (event.key === "Escape") closeLightbox();
      if (event.key === "ArrowLeft") step(-1);
      if (event.key === "ArrowRight") step(1);
    });

    function openLightbox(index) {
      var item = items[index];
      var img = item.querySelector("img");
      var caption = item.getAttribute("data-caption") || "";
      lightbox.img.src = img.getAttribute("data-full") || img.src;
      lightbox.img.alt = img.alt || "";
      lightbox.caption.textContent = caption;
      lightbox.root.classList.add("is-open");
      document.body.style.overflow = "hidden";
      lightbox.closeBtn.focus();
    }

    function closeLightbox() {
      lightbox.root.classList.remove("is-open");
      document.body.style.overflow = "";
    }

    function step(direction) {
      currentIndex = (currentIndex + direction + items.length) % items.length;
      openLightbox(currentIndex);
    }
  });

  function buildLightbox() {
    var root = document.createElement("div");
    root.className = "lightbox";
    root.setAttribute("role", "dialog");
    root.setAttribute("aria-modal", "true");
    root.setAttribute("aria-label", "Image viewer");

    root.innerHTML =
      '<button type="button" class="lightbox__close" aria-label="Close image viewer">&times;</button>' +
      '<button type="button" class="lightbox__prev" aria-label="Previous image">&#8249;</button>' +
      '<figure class="lightbox__figure">' +
      '<img src="" alt="" />' +
      '<figcaption class="lightbox__caption"></figcaption>' +
      "</figure>" +
      '<button type="button" class="lightbox__next" aria-label="Next image">&#8250;</button>';

    return {
      root: root,
      closeBtn: root.querySelector(".lightbox__close"),
      prevBtn: root.querySelector(".lightbox__prev"),
      nextBtn: root.querySelector(".lightbox__next"),
      img: root.querySelector("img"),
      caption: root.querySelector(".lightbox__caption"),
    };
  }
})();
