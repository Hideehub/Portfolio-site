/* Theme toggle, mobile navigation and scroll reveal. Loaded in <head>, so the theme is set before paint. */
(function () {
  "use strict";

  var root = document.documentElement;
  var STORAGE_KEY = "theme";

  function readTheme() {
    try {
      return localStorage.getItem(STORAGE_KEY);
    } catch (e) {
      return null;
    }
  }

  function saveTheme(theme) {
    try {
      localStorage.setItem(STORAGE_KEY, theme);
    } catch (e) {
      /* Storage unavailable (private mode, blocked cookies): theme lasts for this page only. */
    }
  }

  // Dark is the default; light applies only when chosen with the toggle.
  function currentTheme() {
    return root.dataset.theme || "dark";
  }

  var saved = readTheme();
  if (saved === "light" || saved === "dark") {
    root.dataset.theme = saved;
  }
  root.classList.add("js");

  document.addEventListener("DOMContentLoaded", function () {
    var themeToggle = document.querySelector(".theme-toggle");
    if (themeToggle) {
      var syncToggle = function () {
        themeToggle.setAttribute("aria-pressed", String(currentTheme() === "dark"));
      };
      themeToggle.hidden = false;
      syncToggle();
      themeToggle.addEventListener("click", function () {
        var next = currentTheme() === "dark" ? "light" : "dark";
        root.dataset.theme = next;
        saveTheme(next);
        syncToggle();
      });
    }

    var navToggle = document.querySelector(".nav-toggle");
    var nav = document.getElementById("site-nav");
    if (navToggle && nav) {
      var setOpen = function (open) {
        nav.classList.toggle("is-open", open);
        navToggle.setAttribute("aria-expanded", String(open));
      };
      navToggle.hidden = false;
      navToggle.addEventListener("click", function () {
        setOpen(navToggle.getAttribute("aria-expanded") !== "true");
      });
      nav.addEventListener("click", function (event) {
        if (event.target.closest("a")) setOpen(false);
      });
      document.addEventListener("keydown", function (event) {
        if (event.key === "Escape" && navToggle.getAttribute("aria-expanded") === "true") {
          setOpen(false);
          navToggle.focus();
        }
      });
    }

    // Fade sections in as they scroll into view. Without IntersectionObserver, show everything.
    var revealItems = document.querySelectorAll(".reveal");
    if (!("IntersectionObserver" in window)) {
      revealItems.forEach(function (el) { el.classList.add("is-visible"); });
    } else {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
      revealItems.forEach(function (el) { observer.observe(el); });
    }
  });
})();
