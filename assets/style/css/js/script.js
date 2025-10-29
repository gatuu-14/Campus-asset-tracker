// static/js/script.js

document.addEventListener("DOMContentLoaded", function () {
    console.log(" Script loaded successfully!");

    // --- Sidebar toggle for smaller screens ---
    const sidebarToggle = document.querySelector("#sidebarToggle");
    const sidebar = document.querySelector(".sidebar");

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener("click", () => {
            sidebar.classList.toggle("active");
        });
    }

    // --- Auto-dismiss alert messages after 3 seconds ---
    const alerts = document.querySelectorAll(".alert");
    alerts.forEach((alert) => {
        setTimeout(() => {
            alert.style.transition = "opacity 0.5s";
            alert.style.opacity = "0";
            setTimeout(() => alert.remove(), 500);
        }, 3000);
    });

    // --- Simple confirmation before delete ---
    const deleteButtons = document.querySelectorAll(".btn-delete");
    deleteButtons.forEach((btn) => {
        btn.addEventListener("click", (e) => {
            if (!confirm("Are you sure you want to delete this asset?")) {
                e.preventDefault();
            }
        });
    });

    // --- Highlight active sidebar link ---
    const currentPath = window.location.pathname;
    document.querySelectorAll(".nav-link").forEach((link) => {
        if (link.href.includes(currentPath)) {
            link.classList.add("active");
        }
    });

    // --- Show current date in dashboard header ---
    const dateElement = document.querySelector("#currentDate");
    if (dateElement) {
        const today = new Date();
        dateElement.textContent = today.toDateString();
    }
});
