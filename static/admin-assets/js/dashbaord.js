$(document).ready(function () {
    $('#full_year').text(new Date().getFullYear());
});
function Loader(formID) {
    if ($('#' + formID).length) {
        if ($('#' + formID).valid()) {
            $('body').append('<div id="loading"><i class="fas fa-spinner"></i></div>');
            $('body').css('pointer-events', 'none');
            $('.btn').css('pointer-events', 'none');
        }
    } else {
        $('body').append('<div id="loading"><i class="fas fa-spinner"></i></div>');
        $('body').css('pointer-events', 'none');
        $('.btn').css('pointer-events', 'none');
    }
}
var swiper = new Swiper(".mySwiper", {
    spaceBetween: 10,
    slidesPerView: 4,
    freeMode: true,
    watchSlidesProgress: true,
});
var swiper2 = new Swiper(".mySwiper2", {
    spaceBetween: 10,
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    thumbs: {
        swiper: swiper,
    },
});
$(document).ready(function () {
    $(".mob-filter a").click(function () {
        $(".property_list").addClass("open-filter");
    });
    $(".close-filter").click(function () {
        $(".property_list").removeClass("open-filter");
    });
});
//Listing View
$(document).ready(function () {
    $('#grd1').click(function () {
        $('.proListRow').children('.proListItem').addClass('col-xl-4');
        $('.proListRow').children('.proListItem').removeClass('col-xl-12');
        $('.proListRow').children('.proListItem').addClass('col-lg-4');
        $('.proListRow').children('.proListItem').removeClass('col-lg-12');
        $('#grd1').addClass('active');
        $('#lst1').removeClass('active');
    });
    $('#lst1').click(function () {
        $('.proListRow').children('.proListItem').addClass('add-lagre-card');
        $('.proListRow').children('.proListItem').removeClass('col-xl-4');
        $('.proListRow').children('.proListItem').addClass('col-lg-12');
        $('.proListRow').children('.proListItem').removeClass('col-lg-4');
        $('#lst1').addClass('active');
        $('#grd1').removeClass('active');
    });
});
$('.counter-count').each(function () {
    $(this).prop('Counter', 0).animate({
        Counter: $(this).text()
    }, {

        //chnage count up speed here
        duration: 4000,
        easing: 'swing',
        step: function (now) {
            $(this).text(Math.ceil(now));
        }
    });
});
var swiper = new Swiper(".reviewSwiper", {
    slidesPerView: 3,
    spaceBetween: 10,
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
});


if (document.querySelector(".range-slider")) {
    var minThumb = document.querySelector(".min-thumb"),
        maxThumb = document.querySelector(".max-thumb"),
        minValue = document.querySelector(".min-value"),
        maxValue = document.querySelector(".max-value"),
        base = document.querySelector(".range-slider"),
        values = document.querySelector(".values"),
        min = Math.floor(parseInt(base.dataset.min) / 1000) * 1000,
        max = Math.ceil(parseInt(base.dataset.max) / 1000) * 1000,
        step = parseInt(base.dataset.step) || 1,
        bar = document.querySelector(".slider-track"),
        barInner = document.querySelector(".slider-track-filled"),
        offset,
        isDown;

    minValue.innerHTML = min;
    maxValue.innerHTML = max;
    try{
        $("#min-price").val(min)
        $("#max-price").val(max)
        $('#min-price').trigger('change');
        $('#max-price').trigger('change');
    }catch(err){

    }

    function minMaxThumbMoveStart(e) {
        if (e.buttons > 1) {
            return false;
        }

        if (e.target.classList.contains("min-thumb")) {
            minThumb.classList.add("min-down");
        } else if (e.target.classList.contains("max-thumb")) {
            maxThumb.classList.add("max-down");
        }

        base.classList.add("move-start");
        document.addEventListener("mouseup", minMaxThumbMoveEnd);
        document.addEventListener("mousemove", minMaxThumbMove);

        document.addEventListener("touchstart", minMaxThumbMoveEnd);
        document.addEventListener("touchmove", minMaxThumbMove);
    }

    function calculateMinValues(leftPos) {
        var minVal =
            (leftPos / (bar.offsetWidth - minThumb.offsetWidth)) * (max - min) + min;
        var multi = Math.floor(minVal / step);
        minVal = step * multi;

        //var minVal = Math.round(leftPos / step) * step + min;
        minValue.innerHTML = minVal;
        try{
            $("#min-price").val(minVal)
            $('#min-price').trigger('change');
        }catch(err){
    
        }
    }

    function calculateMaxValues(leftPos) {
        var maxVal =
            (leftPos / (bar.offsetWidth - maxThumb.offsetWidth)) * (max - min) + min;
        var multi = Math.floor(maxVal / step);
        maxVal = step * multi;
        maxValue.innerHTML = maxVal;
        try{
            $("#max-price").val(maxVal)
            $('#max-price').trigger('change');
        }catch(err){
    
        }
    }

    function minMaxThumbMove(e) {
        var mousePosition = {};
        if (base.classList.contains("move-start")) {
            if (!e.touches) {
                mousePosition = {
                    x: e.clientX
                };
            } else {
                mousePosition = {
                    x: e.touches[0].clientX
                };
            }
            var leftPos = Math.max(
                0,
                Math.min(
                    mousePosition.x -
                    base.getBoundingClientRect().left -
                    minThumb.offsetWidth / 2,
                    bar.offsetWidth - minThumb.offsetWidth
                )
            );
            var percentage = (leftPos / bar.offsetWidth) * 100;
            if (minThumb.classList.contains("min-down")) {
                var cPos = Math.min(
                    percentage,
                    (maxThumb.offsetLeft / bar.offsetWidth) * 100
                );
                minThumb.style.left = cPos + "%";
                calculateMinValues((cPos * bar.offsetWidth) / 100);
            } else if (maxThumb.classList.contains("max-down")) {
                var cPos = Math.max(
                    percentage,
                    (minThumb.offsetLeft / bar.offsetWidth) * 100
                );
                maxThumb.style.left = cPos + "%";
                calculateMaxValues((cPos * bar.offsetWidth) / 100);
            }
            calculateFilledTrackWidth();
        }
    }

    function calculateFilledTrackWidth() {
        barInner.style.marginLeft =
            (minThumb.offsetLeft / bar.offsetWidth) * 100 + "%";
        barInner.style.width =
            ((maxThumb.offsetLeft - minThumb.offsetLeft) / bar.offsetWidth) * 100 + "%";
    }

    function minMaxThumbMoveEnd(e) {
        base.classList.remove("move-start");
        minThumb.classList.remove("min-down");
        maxThumb.classList.remove("max-down");
        document.removeEventListener("mouseup", minMaxThumbMoveEnd);
        document.removeEventListener("mousemove", minMaxThumbMove);
        document.removeEventListener("touchstart", minMaxThumbMoveEnd);
        document.removeEventListener("touchmove", minMaxThumbMove);
    }

    function onSliderTrackClick(e) {
        var distanceMinThumb = Math.hypot(
            minThumb.getBoundingClientRect().x - parseInt(e.clientX),
            minThumb.getBoundingClientRect().y - parseInt(e.clientY)
        );
        var distanceMaxThumb = Math.hypot(
            maxThumb.getBoundingClientRect().x - parseInt(e.clientX),
            maxThumb.getBoundingClientRect().y - parseInt(e.clientY)
        );
        var leftPos = Math.max(
            0,
            Math.min(
                e.clientX - 30 - minThumb.offsetWidth / 2,
                bar.offsetWidth - minThumb.offsetWidth
            )
        );
        var percentage = (leftPos / bar.offsetWidth) * 100;
        if (distanceMinThumb < distanceMaxThumb) {
            minThumb.style.left = percentage + "%";
            calculateMinValues(leftPos);
        } else {
            maxThumb.style.left = percentage + "%";
            calculateMaxValues(leftPos);
        }
        calculateFilledTrackWidth();
    }

    bar.addEventListener("mousedown", onSliderTrackClick);

    document.addEventListener("mousedown", minMaxThumbMoveStart);
    document.addEventListener("touchstart", minMaxThumbMoveStart);

    document.addEventListener("mouseup", minMaxThumbMoveEnd);
    document.addEventListener("touchend", minMaxThumbMoveEnd);
}
