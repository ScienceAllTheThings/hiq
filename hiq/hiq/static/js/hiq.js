$(document).ready(function(){
  // Paralax effect when scrolling
  var lastScrollTop = 0;
  $(window).scroll(function(){
     var st = $(this).scrollTop();
     if (st > lastScrollTop){
         // downscroll code
         $('.hero-container').css('top',parseInt($('.hero-container').css('top'))-1 + 'px');
         $('.paralax-container').css('top',parseInt($('.paralax-container').css('top'))-5 + 'px');
     } else {
        // upscroll code
        $('.hero-container').css('top',parseInt($('.hero-container').css('top'))+1 + 'px');
        $('.paralax-container').css('top',parseInt($('.paralax-container').css('top'))+5 + 'px');
     }
     lastScrollTop = st;
  })

  $('.scroll-down').click(function(){
    $('html, body').animate({
    scrollTop: $(".paralax-container").offset().top / 2
 }, 1000);
    $('.scroll-down').hide();

  })


  // Signupform submit
  $('#signupform_submit').click(function(){
    $('form[name="signupform"] button[type="submit"]').click();
  })

  // Verify form submit
  $('form[name="verifyform"] .verify-submit').click(function() {
    $('form[name="verifyform"] button[type="submit"]').click();
  })

  // Slide animation for questions
  $('.nav .next').click(function(){
    var current_num = $('.question.active').data('question_number');
    $('.question.active').removeClass('active');
    $('.question[data-question_number="'+(current_num+1)+'"]').addClass('active');
    $('.nav .prev').show();
  })

  $('.nav .prev').click(function() {
    var current_num = $('.question.active').data('question_number');
    $('.question.active').removeClass('active');
    $('.question[data-question_number="'+(current_num-1)+'"]').addClass('active');
    if (current_num-1 == 1) {
      $(this).hide();
    }
  })
})
