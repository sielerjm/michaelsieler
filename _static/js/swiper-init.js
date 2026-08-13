document.addEventListener("DOMContentLoaded", function () {
    if (typeof Swiper === "undefined") {
        return;
    }

    document.querySelectorAll(".mySwiper").forEach(function (el) {
        new Swiper(el, {
            loop: true,
            pagination: {
                el: el.querySelector(".swiper-pagination"),
                clickable: true
            },
            navigation: {
                nextEl: el.querySelector(".swiper-button-next"),
                prevEl: el.querySelector(".swiper-button-prev")
            }
        });
    });
});
