const nav = document.getElementById("site-nav");
const toggle = document.getElementById("nav-toggle");

const onScroll = () => {
  if (!nav) return;
  nav.classList.toggle("is-scrolled", window.scrollY > 24);
};
onScroll();
window.addEventListener("scroll", onScroll, { passive: true });

if (toggle && nav) {
  toggle.addEventListener("click", () => {
    const open = nav.classList.toggle("is-open");
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  });
  nav.querySelectorAll(".nav__links a").forEach((link) => {
    link.addEventListener("click", () => nav.classList.remove("is-open"));
  });
}

const videoTriggers = document.querySelectorAll(".js-video-trigger[data-video-id]");
videoTriggers.forEach((trigger) => {
  const videoId = trigger.dataset.videoId;
  if (!videoId) return;
  const loadVideo = () => {
    const iframe = document.createElement("iframe");
    iframe.src = `https://www.youtube-nocookie.com/embed/${videoId}?autoplay=1`;
    iframe.title = trigger.dataset.title || "Video";
    iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
    iframe.allowFullscreen = true;
    iframe.referrerPolicy = "strict-origin-when-cross-origin";
    iframe.style.position = "absolute";
    iframe.style.inset = "0";
    iframe.style.border = "0";
    iframe.style.width = "100%";
    iframe.style.height = "100%";
    const parent = trigger.parentElement;
    const wrapper = document.createElement("div");
    wrapper.className = "embed";
    wrapper.style.position = "relative";
    wrapper.style.width = "100%";
    wrapper.style.paddingTop = "56.25%";
    wrapper.style.background = "#000";
    wrapper.style.margin = "0";
    wrapper.appendChild(iframe);
    parent.replaceChild(wrapper, trigger);
  };
  trigger.addEventListener("click", loadVideo, { once: true });
  trigger.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      loadVideo();
    }
  }, { once: true });
});

// Testimony category filtering (Static, no reload)
const filterButtons = document.querySelectorAll(".js-testimony-filters .filter-pill");
const testimonyCards = document.querySelectorAll(".testimony-card");
const featuredTestimony = document.querySelector(".testimony-feature");

if (filterButtons.length) {
  filterButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      filterButtons.forEach((b) => b.classList.remove("is-on"));
      btn.classList.add("is-on");
      const category = btn.dataset.filter;

      testimonyCards.forEach((card) => {
        if (category === "all" || card.dataset.category === category) {
          card.style.display = "";
        } else {
          card.style.display = "none";
        }
      });

      if (featuredTestimony) {
        if (category === "all" || featuredTestimony.dataset.category === category) {
          featuredTestimony.style.display = "";
        } else {
          featuredTestimony.style.display = "none";
        }
      }
    });
  });
}

// In-page testimony modal
const dialog = document.getElementById("testimony-dialog");
const modalClose = document.getElementById("modal-close");
const modalCategory = document.getElementById("modal-category");
const modalTitle = document.getElementById("modal-title");
const modalMeta = document.getElementById("modal-meta");
const modalStory = document.getElementById("modal-story");

document.addEventListener("click", (e) => {
  const trigger = e.target.closest(".js-open-testimony");
  if (!trigger || !dialog) return;

  if (modalCategory) modalCategory.textContent = trigger.dataset.category || "";
  if (modalTitle) modalTitle.textContent = trigger.dataset.title || "";
  if (modalMeta) {
    const metaParts = [trigger.dataset.name, trigger.dataset.location].filter(Boolean);
    modalMeta.textContent = metaParts.join(" · ");
  }
  if (modalStory) {
    modalStory.innerHTML = `<p>${(trigger.dataset.story || "").replace(/\n+/g, "</p><p>")}</p>`;
  }

  if (typeof dialog.showModal === "function") {
    dialog.showModal();
  } else {
    dialog.setAttribute("open", "");
  }
});

if (modalClose && dialog) {
  modalClose.addEventListener("click", () => {
    if (typeof dialog.close === "function") {
      dialog.close();
    } else {
      dialog.removeAttribute("open");
    }
  });
}

if (dialog) {
  dialog.addEventListener("click", (e) => {
    if (e.target === dialog) {
      if (typeof dialog.close === "function") {
        dialog.close();
      } else {
        dialog.removeAttribute("open");
      }
    }
  });
}
