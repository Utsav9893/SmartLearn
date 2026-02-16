document.addEventListener('DOMContentLoaded', () => {
    
    // 1. Navbar Scroll Effect
    const nav = document.querySelector('nav');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) nav.classList.add('scrolled');
        else nav.classList.remove('scrolled');
    });
    // 1. Hero Slider Logic
    const slides = document.querySelectorAll('.slide');
    const dots = document.querySelectorAll('.dot');
    let currentSlide = 0;

    if (slides.length > 0) {
        const showSlide = (n) => {
            slides.forEach(s => s.classList.remove('active'));
            dots.forEach(d => d.classList.remove('active'));
            currentSlide = (n + slides.length) % slides.length;
            slides[currentSlide].classList.add('active');
            dots[currentSlide].classList.add('active');
        };

        setInterval(() => showSlide(currentSlide + 1), 5000);

        dots.forEach((dot, i) => {
            dot.addEventListener('click', () => showSlide(i));
        });
    }

    // 2. Localization: Update Enroll Toast to INR
    window.enrollNow = (courseName) => {
        const toast = document.createElement('div');
        toast.className = 'glass-card';
        toast.style.cssText = `
            position: fixed; bottom: 30px; right: 30px; 
            padding: 15px 30px; border-left: 4px solid #22c55e;
            z-index: 9999; animation: slideIn 0.5s ease;
        `;
        toast.innerHTML = `<span>✅ Success! You've enrolled in ${courseName}. Check your email for the receipt.</span>`;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 4000);
    };
    
    // 2. Course Filtering Logic (Search & Category)
    const searchInput = document.getElementById('courseSearch');
    const filterButtons = document.querySelectorAll('.filter-btn');
    const courseCards = document.querySelectorAll('.course-card');

    const filterCourses = () => {
        const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
        const activeBtn = document.querySelector('.filter-btn.active');
        const activeCategory = activeBtn ? activeBtn.dataset.category : 'all';

        courseCards.forEach(card => {
            const title = card.querySelector('h3').innerText.toLowerCase();
            const category = card.dataset.category;
            
            const matchesSearch = title.includes(searchTerm);
            const matchesCategory = activeCategory === 'all' || category === activeCategory;

            if (matchesSearch && matchesCategory) {
                card.style.display = 'block';
                card.style.opacity = '1';
            } else {
                card.style.display = 'none';
            }
        });
    };

    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            filterButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            filterCourses();
        });
    });

    if (searchInput) {
        searchInput.addEventListener('input', filterCourses);
    }

    // 3. Counter Animation (About Page)
    const counters = document.querySelectorAll('.counter');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = +counter.getAttribute('data-target');
                let count = 0;
                const increment = target / 50;

                const updateCount = () => {
                    if (count < target) {
                        count += increment;
                        counter.innerText = Math.ceil(count);
                        setTimeout(updateCount, 25);
                    } else {
                        counter.innerText = target;
                    }
                };
                updateCount();
                observer.unobserve(counter);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(c => observer.observe(c));

    // 4. Global Notification System
    window.enrollNow = (msg) => {
        const toast = document.createElement('div');
        toast.className = 'glass-card toast-notification';
        toast.style.cssText = `
            position: fixed; bottom: 30px; right: 30px; 
            padding: 15px 30px; border-left: 4px solid var(--primary);
            z-index: 9999; animation: slideIn 0.5s ease forwards;
        `;
        toast.innerHTML = `<span>🎉 ${msg}</span>`;
        document.body.appendChild(toast);
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 500);
        }, 3000);
    };
});
