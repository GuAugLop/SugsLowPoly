/* Sug's LowPoly — small progressive enhancements. The site works without JavaScript. */
(function () {
  "use strict";
  var doc = document;
  doc.documentElement.classList.add("js");

  // mobile navigation
  var toggle = doc.querySelector(".nav-toggle");
  var nav = doc.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.tagName === "A") { nav.classList.remove("open"); toggle.setAttribute("aria-expanded", "false"); }
    });
  }

  // current year in the footer
  var year = doc.getElementById("year");
  if (year) year.textContent = String(new Date().getFullYear());

  // reveal on scroll
  var items = doc.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && items.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add("in"); });
  }

  // decorative embers in the hero
  var embers = doc.querySelector(".embers");
  var calm = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (embers && !calm) {
    for (var i = 0; i < 22; i++) {
      var e = doc.createElement("i");
      var size = 2 + Math.random() * 4;
      e.style.left = (Math.random() * 100).toFixed(1) + "%";
      e.style.width = e.style.height = size.toFixed(1) + "px";
      e.style.animationDuration = (9 + Math.random() * 12).toFixed(1) + "s";
      e.style.animationDelay = (-Math.random() * 20).toFixed(1) + "s";
      e.style.setProperty("--dx", (Math.random() * 160 - 80).toFixed(0) + "px");
      embers.appendChild(e);
    }
  }

  // gallery lightbox
  var tiles = Array.prototype.slice.call(doc.querySelectorAll("[data-full]"));
  if (!tiles.length) return;
  var box = doc.createElement("div");
  box.className = "lightbox";
  box.setAttribute("role", "dialog");
  box.setAttribute("aria-modal", "true");
  box.setAttribute("aria-label", "Image viewer");
  box.innerHTML =
    '<button class="lb-btn lb-close" type="button" aria-label="Close"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="square"><path d="M5 5l14 14M19 5L5 19"/></svg></button>' +
    '<button class="lb-btn lb-prev" type="button" aria-label="Previous image"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="square"><path d="M15 4l-8 8 8 8"/></svg></button>' +
    '<figure><img alt=""><figcaption></figcaption></figure>' +
    '<button class="lb-btn lb-next" type="button" aria-label="Next image"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="square"><path d="M9 4l8 8-8 8"/></svg></button>';
  doc.body.appendChild(box);
  var img = box.querySelector("img"), cap = box.querySelector("figcaption"), index = 0, last = null;

  function show(i) {
    index = (i + tiles.length) % tiles.length;
    var t = tiles[index];
    img.src = t.getAttribute("data-full");
    img.alt = t.getAttribute("data-caption") || "";
    cap.textContent = (index + 1) + " / " + tiles.length + "  ·  " + (t.getAttribute("data-caption") || "");
  }
  function open(i) { last = doc.activeElement; show(i); box.classList.add("open"); doc.body.style.overflow = "hidden"; box.querySelector(".lb-close").focus(); }
  function close() { box.classList.remove("open"); doc.body.style.overflow = ""; img.removeAttribute("src"); if (last) last.focus(); }

  tiles.forEach(function (t, i) { t.addEventListener("click", function (e) { e.preventDefault(); open(i); }); });
  box.querySelector(".lb-close").addEventListener("click", close);
  box.querySelector(".lb-prev").addEventListener("click", function () { show(index - 1); });
  box.querySelector(".lb-next").addEventListener("click", function () { show(index + 1); });
  box.addEventListener("click", function (e) { if (e.target === box) close(); });
  doc.addEventListener("keydown", function (e) {
    if (!box.classList.contains("open")) return;
    if (e.key === "Escape") close();
    else if (e.key === "ArrowLeft") show(index - 1);
    else if (e.key === "ArrowRight") show(index + 1);
    else if (e.key === "Tab") {
      var f = box.querySelectorAll("button"), first = f[0], lastBtn = f[f.length - 1];
      if (e.shiftKey && doc.activeElement === first) { e.preventDefault(); lastBtn.focus(); }
      else if (!e.shiftKey && doc.activeElement === lastBtn) { e.preventDefault(); first.focus(); }
    }
  });
})();
