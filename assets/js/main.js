/* Navigation and progressive enhancement for service-request pages. */
(function () {
  "use strict";
  var d = document, header = d.querySelector(".site-header");
  if (header) {
    var onScroll = function () { header.classList.toggle("scrolled", window.scrollY > 8); };
    onScroll(); window.addEventListener("scroll", onScroll, { passive: true });
  }
  var toggle = d.querySelector(".nav-toggle"), nav = d.querySelector(".nav"), backdrop = d.querySelector(".nav-backdrop");
  function setDropdown(group, open) {
    var button = group.querySelector("[data-services-toggle]"), menu = group.querySelector(".dropdown");
    group.classList.toggle("open", open); if (button) button.setAttribute("aria-expanded", String(open));
    if (menu) menu.hidden = !open;
  }
  function setNav(open, returnFocus) {
    if (!nav || !toggle) return;
    var mobile = window.innerWidth <= 1000;
    nav.classList.toggle("open", open); toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    if (backdrop) backdrop.classList.toggle("show", open);
    d.body.style.overflow = open && mobile ? "hidden" : "";
    d.querySelectorAll("main,.site-footer,.site-header .brand").forEach(function (e) { e.inert = open && mobile; });
    if (open && mobile) { nav.setAttribute("role", "dialog"); nav.setAttribute("aria-modal", "true"); }
    else { nav.removeAttribute("role"); nav.removeAttribute("aria-modal"); }
    if (!open) nav.querySelectorAll(".has-dropdown").forEach(function (g) { setDropdown(g, false); });
    if (open && mobile) { var first = nav.querySelector(".nav-close"); if (first) first.focus(); }
    else if (returnFocus) toggle.focus();
  }
  if (toggle) toggle.addEventListener("click", function () { setNav(!nav.classList.contains("open"), true); });
  if (backdrop) backdrop.addEventListener("click", function () { setNav(false, true); });
  var close = nav && nav.querySelector(".nav-close");
  if (close) close.addEventListener("click", function () { setNav(false, true); });
  d.querySelectorAll(".has-dropdown").forEach(function (group) {
    var button = group.querySelector("[data-services-toggle]"); if (!button) return;
    button.addEventListener("click", function () { setDropdown(group, button.getAttribute("aria-expanded") !== "true"); });
    group.addEventListener("mouseenter", function () { if (window.innerWidth > 1000) setDropdown(group, true); });
    group.addEventListener("mouseleave", function () { if (window.innerWidth > 1000 && !group.contains(d.activeElement)) setDropdown(group, false); });
    group.addEventListener("focusout", function (event) { if (!group.contains(event.relatedTarget)) setDropdown(group, false); });
  });
  if (nav) nav.querySelectorAll("a").forEach(function (a) { a.addEventListener("click", function () { setNav(false, false); }); });
  d.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      var group = d.querySelector(".has-dropdown.open");
      if (group) { setDropdown(group, false); group.querySelector("[data-services-toggle]").focus(); }
      else if (nav && nav.classList.contains("open")) setNav(false, true);
    }
    if (event.key === "Tab" && nav && nav.classList.contains("open") && window.innerWidth <= 1000) {
      var items = Array.from(nav.querySelectorAll("a,button")).filter(function (e) { return !e.disabled && e.getClientRects().length && !e.closest("[hidden]"); });
      var first = items[0], last = items[items.length - 1];
      if (event.shiftKey && (d.activeElement === first || !nav.contains(d.activeElement))) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && (d.activeElement === last || !nav.contains(d.activeElement))) { event.preventDefault(); first.focus(); }
    }
  });
  window.addEventListener("resize", function () { if (window.innerWidth > 1000) setNav(false, false); });
  // Keep content visible even if any script fails. Motion is CSS-only and limited to the hero.
  d.querySelectorAll("[data-year]").forEach(function (e) { e.textContent = new Date().getFullYear(); });
  var mbar = d.querySelector(".mobile-bar"), qform = d.querySelector("form[data-quote-form]");
  if (mbar && qform && "IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) { mbar.classList.toggle("is-hidden", entries[0].isIntersecting); }, { threshold: 0.2 }).observe(qform);
  }
})();

/* Receipt-confirmed enquiries. Keep field IDs compatible with the intake workflow. */
(function () {
  "use strict";
  var d = document;
  var webhook = "https://auto.sdagents.ai/webhook/hvac-sites";
  var forms = d.querySelectorAll("form[data-quote-form], form[data-enquiry-form]");
  var receiptKey = "hvac-enquiry-receipt-v1";
  var contextKey = "hvac-enquiry-context-v1", attributionKey = "hvac-enquiry-attribution-v1";
  var attributionNames = ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "gclid", "gbraid", "wbraid", "fbclid", "msclkid"];
  function recent(key) {
    try { var entry = JSON.parse(sessionStorage.getItem(key) || "null"); return entry && entry.domain === location.hostname && Date.now() - entry.at >= 0 && Date.now() - entry.at < 1800000 ? entry : null; } catch (_) { return null; }
  }
  function sourceWithAttribution(raw) {
    var source = new URL(raw, location.origin);
    if (source.origin !== location.origin) return location.href;
    var prior = recent(attributionKey);
    attributionNames.forEach(function (name) { if (!source.searchParams.has(name) && prior && prior.params && typeof prior.params[name] === "string") source.searchParams.set(name, prior.params[name]); });
    return source.href;
  }
  var arrival = new URL(location.href), attribution = {};
  attributionNames.forEach(function (name) { if (arrival.searchParams.has(name)) attribution[name] = arrival.searchParams.get(name).slice(0, 4096); });
  try { if (Object.keys(attribution).length) sessionStorage.setItem(attributionKey, JSON.stringify({ domain: location.hostname, at: Date.now(), params: attribution })); } catch (_) {}
  var confirmation = d.querySelector("[data-enquiry-confirmation]");
  if (confirmation) {
    try {
      var receipt = JSON.parse(sessionStorage.getItem(receiptKey) || "null");
      if (receipt && receipt.domain === location.hostname && ["email", "phone"].includes(receipt.channel) && Date.now() - receipt.at >= 0 && Date.now() - receipt.at < 1800000) {
        confirmation.querySelector("[data-confirmation-badge]").classList.remove("ty__status-neutral");
        confirmation.querySelectorAll("[data-status-icon]").forEach(function (e) { e.hidden = e.dataset.statusIcon !== "received"; });
        confirmation.querySelectorAll("[data-followup-icon]").forEach(function (e) { e.hidden = e.dataset.followupIcon !== receipt.channel; });
        confirmation.querySelector("[data-confirmation-heading]").textContent = "Request received";
        confirmation.querySelector("[data-confirmation-message]").textContent = "Your request has been received for review. Coverage, pricing, availability and any appointment require separate confirmation.";
        confirmation.querySelector("[data-confirmation-followup]").textContent = receipt.channel === "email" ? "Watch your email for follow-up from the team, including your junk folder." : "Answer the call. It may come from an unfamiliar number or area code.";
      }
    } catch (_) { /* The neutral page remains useful when storage is unavailable. */ }
  }

  function focusQuote() {
    if (window.location.hash !== "#quote") return;
    var form = d.getElementById("quote");
    if (!form) return;
    var header = d.querySelector(".site-header");
    form.style.scrollMarginTop = Math.max(24, (header ? header.getBoundingClientRect().bottom : 0) + 24) + "px";
    form.scrollIntoView({ block: "start", behavior: "instant" });
    var first = form.querySelector('input[name="name"]');
    if (first) first.focus({ preventScroll: true });
  }
  d.addEventListener("click", function (event) {
    var link = event.target.closest && event.target.closest('a[href]');
    if (!link) return;
    var destination = new URL(link.href, window.location.href);
    if (destination.origin === window.location.origin && destination.pathname === window.location.pathname && destination.hash === "#quote") requestAnimationFrame(focusQuote);
  });
  window.addEventListener("hashchange", focusQuote);
  window.addEventListener("load", focusQuote, { once: true });
  if (window.location.hash === "#quote") requestAnimationFrame(focusQuote);

  forms.forEach(function (form) {
    if (form.dataset.leadSubmitBound === "true") return;
    form.dataset.leadSubmitBound = "true";
    var busy = false;
    var received = false;
    var status = form.querySelector(".form-status");
    var button = form.querySelector('button[type="submit"]');
    var preferred = form.querySelector('[name="preferred_contact"]');
    var readiness = form.querySelector("[data-form-readiness]");
    var interest = form.querySelector('[name="service"]');
    var contactPage = location.pathname === "/contact/", previous = recent(contextKey);
    function allowedInterest(value) { return interest && Array.from(interest.options).some(function (o) { return o.value === value; }); }
    function rememberContext() {
      if (contactPage || !interest) return;
      // Carry only the page path and existing marketing attribution, never form data.
      var source = new URL(location.origin + location.pathname), attributed = new URL(sourceWithAttribution(location.href));
      attributionNames.forEach(function (name) { if (attributed.searchParams.has(name)) source.searchParams.set(name, attributed.searchParams.get(name)); });
      try { sessionStorage.setItem(contextKey, JSON.stringify({ domain: location.hostname, at: Date.now(), interest: interest.value, source: source.href })); } catch (_) {}
    }
    if (interest) {
      var requested = new URLSearchParams(location.search).get("interest");
      if (contactPage && requested && allowedInterest(requested)) interest.value = requested;
      else if (contactPage && !requested && previous && allowedInterest(previous.interest)) interest.value = previous.interest;
      interest.addEventListener("change", rememberContext);
      rememberContext();
    }
    function enquirySource() {
      if (contactPage && previous && typeof previous.source === "string") {
        try { var source = new URL(previous.source); if (source.origin === location.origin && (source.pathname === "/" || /^\/services\/[a-z-]+\/$/.test(source.pathname))) return sourceWithAttribution(source.href); } catch (_) {}
      }
      return sourceWithAttribution(location.href);
    }
    function contactChoice() {
      var choice = preferred ? preferred.value : "email";
      ["email", "phone"].forEach(function (name) {
        var input = form.querySelector('[name="' + name + '"]');
        if (!input) return;
        input.disabled = preferred ? name !== choice : false;
        if (preferred) input.required = name === choice;
        var field = input.closest("[data-contact-field]");
        if (field) { field.hidden = preferred ? name !== choice : false; field.classList.remove("invalid"); }
        input.removeAttribute("aria-invalid");
      });
    }
    if (preferred) preferred.addEventListener("change", contactChoice);
    contactChoice();

    function fieldFor(input) { return input.closest("[data-field], .field > div, .field, label"); }
    function validInput(input) {
      if (input.disabled) return true;
      var value = input.value.trim();
      if (input.type === "checkbox") return !input.required || input.checked;
      if (input.required && !value) return false;
      if (!value) return true;
      if (input.type === "email") return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(value) && input.checkValidity();
      if (input.type === "tel") return /^[+()\d\s.\-]+$/.test(value) && value.replace(/\D/g, "").length >= 10 && value.replace(/\D/g, "").length <= 15;
      if (input.name === "postal") return /^[ABCEGHJ-NPRSTVXY]\d[ABCEGHJ-NPRSTVWXYZ][ -]?\d[ABCEGHJ-NPRSTVWXYZ]\d$/i.test(value);
      return input.checkValidity();
    }
    form.querySelectorAll("input, textarea, select").forEach(function (input) {
      input.addEventListener("input", function () {
        var field = fieldFor(input);
        if (field) field.classList.remove("invalid");
        input.removeAttribute("aria-invalid");
      });
    });
    function showStatus(ok, text) {
      if (!status) return;
      status.className = "form-status " + (ok ? "ok" : "err error");
      status.textContent = text;
    }
    function accepted(ack) {
      if (!ack || typeof ack !== "object" || Array.isArray(ack)) return false;
      var negative = ack.accepted === false || ack.success === false || ack.ok === false || ack.failed === true || ack.rejected === true || ack.receipt === "not_confirmed"
        || Boolean(ack.error) || (Array.isArray(ack.errors) ? ack.errors.length > 0 : Boolean(ack.errors))
        || /^(error|failed|failure|rejected|denied)$/i.test(String(ack.status || ""));
      return !negative && (ack.accepted === true || ack.success === true);
    }
    form.addEventListener("submit", async function (event) {
      event.preventDefault();
      if (busy || received) return;
      var firstInvalid = null;
      form.querySelectorAll("input, textarea, select").forEach(function (input) {
        if (input.disabled || input.name === "website") return;
        var ok = validInput(input);
        var field = fieldFor(input);
        if (field) field.classList.toggle("invalid", !ok);
        input.setAttribute("aria-invalid", String(!ok));
        if (!ok && !firstInvalid) firstInvalid = input;
      });
      if (firstInvalid) {
        showStatus(false, "Please check the highlighted details before sending your request.");
        var details = firstInvalid.closest("details");
        if (details) details.open = true;
        firstInvalid.focus();
        return;
      }
      var value = function (name) {
        var input = form.querySelector('[name="' + name + '"]');
        return input && !input.disabled ? input.value.trim() : "";
      };
      if (value("website")) return;
      var now = new Date();
      var pad = function (x) { return String(x).padStart(2, "0"); };
      var stamp = now.getFullYear() + "-" + pad(now.getMonth() + 1) + "-" + pad(now.getDate()) + " " + pad(now.getHours()) + ":" + pad(now.getMinutes()) + ":" + pad(now.getSeconds());
      var message = value("message");
      var electrical = form.hasAttribute("data-enquiry-form");
      var service = value("service");
      if (service && interest && Array.from(interest.options).some(function (o) { return o.value === service; })) {
        message = (electrical ? "Electrical project: " : "Work requested: ") + interest.options[interest.selectedIndex].text + "\n" + message;
      }
      var payload = new URLSearchParams({
        "1.3": value("name"), "2": value("email"), "3": message, "4": value("phone"),
        "5.1": value("address"), "5.3": value("city"), "5.5": value("postal"),
        source_url: enquirySource(), date_created: stamp, preferred_contact: value("preferred_contact") || "email"
      });
      if (form.querySelector('[name="consent"]')) payload.append("consent", "contact_and_provider_assessment_agreed");
      if (electrical) { payload.append("source_domain", form.dataset.domain); payload.append("trade", "Electrical"); payload.append("service", service); }
      var submittedChannel = payload.get("preferred_contact") === "phone" ? "phone" : "email";
      try { sessionStorage.removeItem(receiptKey); } catch (_) {}
      busy = true;
      if (button) button.disabled = true;
      form.setAttribute("aria-busy", "true");
      showStatus(true, "Sending your request. Please wait for receipt confirmation.");
      var controller = new AbortController();
      var timer = setTimeout(function () { controller.abort(); }, 90000);
      try {
        var response = await fetch(webhook, {
          method: "POST", mode: "cors", headers: { "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8" },
          body: payload.toString(), signal: controller.signal
        });
        if (!response.ok) throw new Error("Receipt unconfirmed");
        var ack = await response.json();
        if (!accepted(ack)) throw new Error("Receipt unconfirmed");
        received = true;
        form.dataset.receiptConfirmed = "true";
        var channel = submittedChannel;
        showStatus(true, "Thank you. Your request has been received for review. Watch for follow-up by " + (channel === "email" ? "email" : "phone call") + ". Coverage, pricing, availability and any appointment require separate confirmation.");
        var stored = false;
        try {
          sessionStorage.removeItem(contextKey); sessionStorage.removeItem(attributionKey);
          sessionStorage.setItem(receiptKey, JSON.stringify({ domain: location.hostname, channel: channel, interest: service, at: Date.now() })); stored = true;
        } catch (_) {}
        if (stored && form.dataset.redirectOnSuccess === "/thank-you/") window.location.href = "/thank-you/";
      } catch (error) {
        showStatus(false, "We could not confirm receipt. Your request may already have reached intake. Your details are still here. Email contact@" + (form.dataset.domain || window.location.hostname) + " to confirm before sending again.");
        if (readiness) { readiness.hidden = false; readiness.firstChild.textContent = "You can also email "; }
      } finally {
        clearTimeout(timer);
        busy = false;
        form.removeAttribute("aria-busy");
        if (button) button.disabled = received;
        if (status) status.focus({ preventScroll: true });
      }
    });
    // Enable only after validation and receipt-confirmed submission are bound.
    form.dataset.formReady = "true";
    if (button) button.disabled = false;
    if (readiness) readiness.hidden = true;
  });
})();
