(function () {
    function getHomeNavbar() {
        // Base template also has a Bootstrap navbar with class "navbar".
        // The homepage navbar contains a ".logo" element, so we target that.
        return Array.from(document.querySelectorAll("nav.navbar")).find((nav) => nav.querySelector(".logo"));
    }

    window.addEventListener("scroll", function () {
        const navbar = getHomeNavbar();
        if (!navbar) return;
        navbar.classList.toggle("scrolled", window.scrollY > 50);
    });

    // BACK TO TOP BUTTON LOGIC
    const backToTopBtn = document.getElementById("back-to-top");
    if (backToTopBtn) {
        window.addEventListener("scroll", () => {
            if (window.scrollY > 300) {
                backToTopBtn.classList.add("show");
            } else {
                backToTopBtn.classList.remove("show");
            }
        });

        backToTopBtn.addEventListener("click", () => {
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }

    // SCROLL ANIMATION (Fade-Up)
    const faders = document.querySelectorAll(".fade-up");
    const appearOptions = { threshold: 0.15, rootMargin: "0px 0px -50px 0px" };

    if ("IntersectionObserver" in window) {
        const appearOnScroll = new IntersectionObserver(function (entries, observer) {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                entry.target.classList.add("active");
                observer.unobserve(entry.target);
            });
        }, appearOptions);

        faders.forEach((fader) => {
            appearOnScroll.observe(fader);
        });
    }
})();

