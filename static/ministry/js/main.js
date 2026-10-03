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

const messageVideoTriggers = document.querySelectorAll(".message-video__trigger[data-video-id]");
let activeMessageTrigger = null;
let previousBodyOverflow = "";

const messageDialog = document.createElement("dialog");
messageDialog.className = "message-modal";
messageDialog.setAttribute("aria-modal", "true");
messageDialog.setAttribute("aria-labelledby", "message-modal-title");
messageDialog.innerHTML = `
  <div class="message-modal__content">
    <button class="message-modal__close" type="button" aria-label="Close video">×</button>
    <div class="message-modal__player"></div>
    <h2 class="message-modal__title" id="message-modal-title"></h2>
    <a class="message-modal__youtube" target="_blank" rel="noopener noreferrer">Can't play here? Open on YouTube</a>
  </div>`;
document.body.appendChild(messageDialog);

const messageDialogClose = messageDialog.querySelector(".message-modal__close");
const messageDialogPlayer = messageDialog.querySelector(".message-modal__player");
const messageDialogTitle = messageDialog.querySelector(".message-modal__title");
const messageDialogYoutube = messageDialog.querySelector(".message-modal__youtube");

const closeMessageDialog = () => {
  if (messageDialog.open) messageDialog.close();
};

messageVideoTriggers.forEach((trigger) => {
  trigger.addEventListener("click", () => {
    if (messageDialog.open) closeMessageDialog();
    activeMessageTrigger = trigger;
    const videoId = encodeURIComponent(trigger.dataset.videoId);
    const start = Math.max(0, Number.parseInt(trigger.dataset.start, 10) || 0);
    const startQuery = start ? `&start=${start}` : "";
    const title = trigger.dataset.videoTitle || "LIVE STREAM";
    const iframe = document.createElement("iframe");
    iframe.src = `https://www.youtube.com/embed/${videoId}?autoplay=1&rel=0&playsinline=1${startQuery}`;
    iframe.referrerPolicy = "strict-origin-when-cross-origin";
    iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; fullscreen";
    iframe.allowFullscreen = true;
    iframe.title = title;
    messageDialogPlayer.replaceChildren(iframe);
    messageDialogTitle.textContent = title;
    messageDialogYoutube.href = `https://www.youtube.com/watch?v=${videoId}`;
    previousBodyOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    messageDialog.showModal();
    messageDialogClose.focus();
  });
});

messageDialogClose.addEventListener("click", closeMessageDialog);
messageDialog.addEventListener("click", (event) => {
  if (event.target === messageDialog) closeMessageDialog();
});
messageDialog.addEventListener("close", () => {
  messageDialogPlayer.replaceChildren();
  document.body.style.overflow = previousBodyOverflow;
  if (activeMessageTrigger) activeMessageTrigger.focus();
  activeMessageTrigger = null;
});
messageDialog.addEventListener("keydown", (event) => {
  if (event.key !== "Tab") return;
  const focusable = Array.from(messageDialog.querySelectorAll("button, a[href], iframe"))
    .filter((element) => !element.hasAttribute("disabled"));
  if (!focusable.length) return;
  const first = focusable[0];
  const last = focusable[focusable.length - 1];
  if (event.shiftKey && document.activeElement === first) {
    event.preventDefault();
    last.focus();
  } else if (!event.shiftKey && document.activeElement === last) {
    event.preventDefault();
    first.focus();
  }
});

const messageCards = document.querySelectorAll(".messages-grid .message-video");
if (messageCards.length && !window.matchMedia("(prefers-reduced-motion: reduce)").matches && "IntersectionObserver" in window) {
  const messageCardObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  document.querySelector(".messages-page").classList.add("is-enhanced");
  messageCards.forEach((card) => messageCardObserver.observe(card));
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

(() => {
  const page = document.querySelector("[data-about-page]");
  if (!page) return;

  const reading = page.querySelector(".about-reading");
  const chapters = Array.from(page.querySelectorAll(".about-chapter"));
  const chapterLinks = Array.from(page.querySelectorAll('.about-chapter-menu a[href^="#"]'));
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const progress = page.querySelector(".about-progress span");
  const nav = document.querySelector(".nav");
  const chapterMenu = page.querySelector(".about-chapter-menu");

  const updateProgress = () => {
    if (!progress) return;
    const scrollable = document.documentElement.scrollHeight - window.innerHeight;
    const percentage = scrollable > 0 ? Math.min(1, window.scrollY / scrollable) : 0;
    progress.style.transform = `scaleX(${percentage})`;
  };

  updateProgress();
  window.addEventListener("scroll", updateProgress, { passive: true });
  window.addEventListener("resize", updateProgress);

  const setCurrentChapter = (id) => {
    chapterLinks.forEach((link) => {
      if (link.hash === `#${id}`) {
        link.setAttribute("aria-current", "location");
      } else {
        link.removeAttribute("aria-current");
      }
    });
  };

  if ("IntersectionObserver" in window && chapters.length) {
    const chapterObserver = new IntersectionObserver((entries) => {
      const visible = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
      if (visible.length) setCurrentChapter(visible[0].target.id);
    }, { rootMargin: "-18% 0px -68% 0px", threshold: 0 });
    chapters.forEach((chapter) => chapterObserver.observe(chapter));
  }

  const revealItems = [];
  chapters.forEach((chapter) => {
    chapter.querySelectorAll(":scope > h2, :scope > p, :scope > figure, :scope > blockquote")
      .forEach((item) => {
        item.classList.add("about-reveal");
        revealItems.push(item);
      });
  });
  if (!reduceMotion && "IntersectionObserver" in window && revealItems.length) {
    const revealObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    revealItems.forEach((item) => revealObserver.observe(item));
    page.classList.add("is-enhanced");
  } else {
    revealItems.forEach((item) => item.classList.add("is-visible"));
  }

  page.addEventListener("click", async (event) => {
    const target = event.target instanceof Element ? event.target : null;
    if (!target) return;

    const link = target.closest('a[href^="#"]');
    if (link && page.contains(link)) {
      const chapter = document.getElementById(link.hash.slice(1));
      if (chapter) {
        event.preventDefault();
        const headerHeight = nav ? nav.getBoundingClientRect().height : 0;
        const menuHeight = window.innerWidth < 1024 && chapterMenu
          ? chapterMenu.getBoundingClientRect().height
          : 0;
        const top = chapter.getBoundingClientRect().top + window.scrollY - headerHeight - menuHeight - 12;
        window.scrollTo({ top, behavior: reduceMotion ? "auto" : "smooth" });
        if (window.location.hash !== link.hash) window.history.pushState(null, "", link.hash);
      }
      return;
    }

    const copyButton = target.closest(".about-copy");
    if (copyButton) {
      const quote = copyButton.closest(".about-quote")?.querySelector(".about-quote__text");
      const chapter = copyButton.closest(".about-chapter");
      if (!quote || !chapter) return;
      const pageLink = `${window.location.origin}${window.location.pathname}#${chapter.id}`;
      const copiedText = `${quote.textContent.trim()}\n${pageLink}`;
      const label = copyButton.getAttribute("aria-label");
      try {
        await navigator.clipboard.writeText(copiedText);
        copyButton.textContent = "Copied";
        copyButton.dataset.copied = "true";
        copyButton.setAttribute("aria-label", "Copied quote and page link");
      } catch (error) {
        console.warn("The quote and page link could not be copied.", error);
        copyButton.textContent = "Failed";
        copyButton.setAttribute("aria-label", "Copy failed");
      }
      window.setTimeout(() => {
        copyButton.textContent = "Copy";
        delete copyButton.dataset.copied;
        copyButton.setAttribute("aria-label", label || "Copy quote and page link");
      }, 2000);
      return;
    }

    const locationButton = target.closest(".about-locations button");
    if (locationButton) {
      page.querySelectorAll(".about-locations button").forEach((button) => {
        button.setAttribute("aria-pressed", String(button === locationButton));
      });
      return;
    }

    const image = target.closest(".about-image");
    if (image) openLightbox(image);
  });

  let textSize = 1;
  const textSizes = ["small", "normal", "large"];
  if (reading) {
    try {
      const savedSize = window.localStorage.getItem("about-text-size");
      const savedIndex = textSizes.indexOf(savedSize);
      if (savedIndex !== -1) textSize = savedIndex;
    } catch (error) {
      console.warn("The saved About page text size could not be read.", error);
    }
    const applyTextSize = () => {
      reading.dataset.textSize = textSizes[textSize];
      page.querySelectorAll("[data-text-step]").forEach((button) => {
        const step = Number(button.dataset.textStep);
        button.disabled = (step < 0 && textSize === 0) || (step > 0 && textSize === textSizes.length - 1);
      });
    };
    applyTextSize();
    page.querySelectorAll("[data-text-step]").forEach((button) => {
      button.addEventListener("click", () => {
        textSize = Math.max(0, Math.min(textSizes.length - 1, textSize + Number(button.dataset.textStep)));
        applyTextSize();
        try {
          window.localStorage.setItem("about-text-size", textSizes[textSize]);
        } catch (error) {
          console.warn("The About page text size could not be saved.", error);
        }
      });
    });
  }

  page.querySelectorAll(".about-image").forEach((image) => {
    image.tabIndex = 0;
    image.setAttribute("role", "button");
    image.setAttribute("aria-label", `Enlarge image: ${image.alt}`);
    image.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        openLightbox(image);
      }
    });
  });

  const lightbox = document.createElement("dialog");
  lightbox.className = "about-lightbox";
  lightbox.setAttribute("aria-label", "Enlarged image");
  const closeButton = document.createElement("button");
  closeButton.type = "button";
  closeButton.className = "about-lightbox__close";
  closeButton.textContent = "Close";
  const lightboxImage = document.createElement("img");
  const caption = document.createElement("p");
  lightbox.append(closeButton, lightboxImage, caption);
  page.appendChild(lightbox);
  let returnFocus = null;

  function openLightbox(image) {
    returnFocus = image;
    lightboxImage.src = image.currentSrc || image.src;
    lightboxImage.alt = image.alt;
    const imageCaption = image.closest("figure")?.querySelector("figcaption");
    caption.textContent = imageCaption ? imageCaption.textContent.trim() : image.alt;
    if (typeof lightbox.showModal === "function") {
      lightbox.showModal();
    } else {
      lightbox.setAttribute("open", "");
    }
    closeButton.focus();
  }

  const closeLightbox = () => {
    if (typeof lightbox.close === "function" && lightbox.open) {
      lightbox.close();
    } else {
      lightbox.removeAttribute("open");
      if (returnFocus) returnFocus.focus();
    }
  };
  closeButton.addEventListener("click", closeLightbox);
  lightbox.addEventListener("close", () => {
    if (returnFocus) returnFocus.focus();
  });
  lightbox.addEventListener("click", (event) => {
    if (event.target === lightbox) closeLightbox();
  });
  lightbox.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && typeof lightbox.close !== "function") closeLightbox();
  });
})();

(() => {
  const page = document.querySelector("[data-about-page]");
  if (!page || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  if (!("IntersectionObserver" in window)) return;

  page.querySelectorAll(".about-scene").forEach((scene) => {
    const stage = scene.querySelector(".about-scene__stage");
    if (!stage) return;
    const photos = Array.from(stage.querySelectorAll(".about-scene__photo[data-photo-for]"));
    const chapters = Array.from(scene.querySelectorAll(".about-chapter[id]"));
    const photoObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const activeId = entry.target.id;
        photos.forEach((photo) => {
          photo.classList.toggle("is-active", photo.dataset.photoFor === activeId);
        });
      });
    }, { rootMargin: "-38% 0px -42% 0px", threshold: 0 });
    chapters.forEach((chapter) => photoObserver.observe(chapter));
  });
})();
