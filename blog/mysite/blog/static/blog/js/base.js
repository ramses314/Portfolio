
$(function(){

	// СЛАЙДЕР ДЛЯ ПОКАЗА СТАТЕЙ О РЕТРО-КИНО
	$('.lenta__container').slick({
		infinite: true,
		slidesToShow: 3,
		slidesToScroll: 1,
        touchThreshold: true,
        arrows: false,
        autoplay: true,
      	autoplaySpeed: 3000,
      	swipe: false,
      	responsive: [
			    {
			      breakpoint: 600,
			      settings: {
			        infinite: true,
					slidesToShow: 2,
					slidesToScroll: 1,
					vertical: false,
			        touchThreshold: true,
			        arrows: false,
			        autoplay: true,
			      	autoplaySpeed: 3000,
			      }
			    },
			     {
			      breakpoint: 400,
			      settings: {
			        infinite: true,
					slidesToShow: 1,
					slidesToScroll: 1,
					vertical: false,
					verticalSwiping: false,

			        touchThreshold: true,
			        arrows: false,
			        autoplay: true,
			      	autoplaySpeed: 3000,
			      }
			    },
  ]
	})


	// СЛАЙДЕР ДЛЯ ПОКАЗАРЕКОМЕНДОВАННЫХ СТАТЕЙ В ДЕТАЙЛ ШАБЛОНЕ
	$('.recomm__items').slick({
		infinite: true,
		slidesToShow: 3,
		slidesToScroll: 1,
        touchThreshold: true,
        arrows: false,
        autoplay: true,
      	autoplaySpeed: 3000,
      	swipe: false,
      	responsive: [
			    {
			      breakpoint: 600,
			      settings: {
			        infinite: true,
					slidesToShow: 2,
					slidesToScroll: 1,
					vertical: false,
			        touchThreshold: true,
			        arrows: false,
			        autoplay: true,
			      	autoplaySpeed: 3000,
			      }
			    },
			     {
			      breakpoint: 400,
			      settings: {
			        infinite: true,
					slidesToShow: 1,
					slidesToScroll: 1,
					vertical: false,
					verticalSwiping: false,

			        touchThreshold: true,
			        arrows: false,
			        autoplay: true,
			      	autoplaySpeed: 3000,
			      }
			    },
  ]
	})


});

