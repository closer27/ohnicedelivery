/*!
 * Start Bootstrap - Agency Bootstrap Theme (http://startbootstrap.com)
 * Code licensed under the Apache License v2.0.
 * For details, see http://www.apache.org/licenses/LICENSE-2.0.
 */

// jQuery for page scrolling feature - requires jQuery Easing plugin
$(function() {
    $('a.page-scroll').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });
});

// Highlight the top nav as scrolling occurs
$('body').scrollspy({
    target: '.navbar-fixed-top'
})

// Closes the Responsive Menu on Menu Item Click
$('.navbar-collapse ul li a').click(function() {
    $('.navbar-toggle:visible').click();
});

/**
 * validate uploaded files
 */
function validateFiles()
{
    var sellers;
    if (navigator.platform === "MacIntel") {
        // macOS
        sellers = ["TEN", "uniq", "%E1%84%8C%E1%85%A5%E1%86%BC%E1%84%87%E1%85%A9",
        "%E1%84%89%E1%85%B3%E1%84%90%E1%85%A9%E1%84%8B%E1%85%A5",
        "%E1%84%87%E1%85%A2%E1%84%89%E1%85%A9%E1%86%BC%E1%84%85%E1%85%B5%E1%84%89%E1%85%B3%E1%84%90%E1%85%B3",
        "orders", "%E1%84%87%E1%85%A9%E1%84%89%E1%85%A1%E1%84%85%E1%85%A1%E1%86%BC"];
    } else {
        // Windows
        sellers = ["TEN", "uniq", "정보", "스토어", "배송리스트", "orders", "보사랑"]
    }

    // initializing
    for (var i=0; i< sellers.length; i++) {
        var elem = document.getElementById(sellers[i]);
        elem.style.backgroundColor = "white";
    }

    var files = document.getElementById('upload_files').files;
    for (var i = 0; i < files.length; ++i) {
      var name = files.item(i).name;

      if (navigator.platform === "MacIntel") {
        name = encodeURI(name);
      }

      var validSellers = [];
      let isAllowedFile = false;

      for (let seller of sellers) {
        if (name.includes(seller)) {
            validSellers.push(seller);
            isAllowedFile = true;
            break;
        }
      }
      if (!isAllowedFile) {
        alert(`${files.item(i).name}은 현재 변환을 지원하지 않는 파일입니다. 쇼핑몰 측에서 파일포맷을 변경했을 수 있으니 관리자에게 문의하세요.`);
      }

      // change css style if relevant file.
      for (var validSeller of validSellers) {
        var relevantSeller;
        if (navigator.platform === "MacIntel") {
            // macOS
            relevantSeller = validSeller;   // just input
        } else {
            // Windows
            relevantSeller = encodeURI(validSeller); // encodeURI once.
        }
        var elem = document.getElementById(relevantSeller);
        elem.style.backgroundColor = "green";
      }
    }
}