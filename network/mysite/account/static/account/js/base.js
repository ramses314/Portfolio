
$(function(){

// 	$(window).resize(function(e){
// 		$('.news__text').text('Ширина:' + window.innerWidth +
// 		 ", высота:" + window.innerHeight + '\n' + 'positionY:' + window.scrollY);
// 	});

// 	$(window).scroll(function(e){
// 		var a = $('.news__text').text()
// 		console.log(a)
// 		$('.news__img').text(a + 'position Y:' + window.scrollY);
// 	})

// 	$('.news').click(function(e){
// 		$('.news__text').text(666)
// 	})

// 	$(window).on('resize scroll', {'user' : 'test111'} ,function(e){
// 		$('.news__text').text('Ширина:' + window.innerWidth +
// 		 ", высота:" + window.innerHeight + '\n' + 'positionY:' + window.scrollY + '\n' + e.data.user);
// 	})

// 	$(window).trigger('scroll')

// 	$('<img>', {
// 		src: 'media/media/posts/2022/08/20/IMG-1356.jpg',
// 		alt: 'loadded 99%',
// 		click : function(e){
// 			$(this).toggleClass('selected')
// 		}
// 	})
// 	.css({
// 		'padding' : '20px',

// 	})
// 	.appendTo('body');

// 	$('.news').slideToggle(2000);

// $('.someDive').on('click', function(e){
// 	var modal = $('.news__img');
// 	console.log(22, (window.innerHeight - modal.height() / 2) )
// 	modal.css('top', (window.innerHeight - modal.height()) / 2);
// 	modal.css('left', (window.innerWidth - modal.width()) / 2);
// })


// PAGE: search__user
// Поиск пользователей (элемент выбора пола)
	$('.followers__gender').on('click', function(e) {

		$('.gender').css({
			'display' : 'none',
		})
	})

	selected = $('.followers__gender option:selected').text()
	var listik = ['Парень', "Девушка"];
	if (listik.includes($('.followers__gender option:selected').text())) {

		$('.gender').css({
			'display' : 'none',
		}) } else {}




	// PAGE: user__profile
	// Просмотр галереи подписчиков

	$('.profile__gallery').on('click', function(e) {

		$('.abs_wrapper').css({
			'display' : 'block'
		})

		$('.abs__abs').css({
			'display' : 'block'
		})

		$('.abs_wrapper').css({'height' : $('.wrapper').height()})
		
		$('.abs_profile__gallery').slick({
		// infinite: true,
  // 		slidesToShow: 1,
  // 		slidesToScroll: 1,
  // 		// dots: true

            // prevArrow: $('.abs__prev'),
            // nextArrow: $('.abs__next'),
		}).slideDown()


		$('.slick-prev').text('❮')
		$('.slick-next').text('❯')



		$(window).on('resize', function(e) {

			var er = $('.content').height(); 
			// console.log(33, er, $('.profile').height(), $('.abs_wrapper').height(), $(window).height(),
			// 	)
			
			// $('.abs_wrapper').css({'height' : er})

			// console.log(34, er, $('.abs_wrapper').height(), $('.profile').height(),
			// 	$('.wrapper').height())
			$('.abs_wrapper').css({'height' : $('.wrapper').height()})
			// if ($(window).height() < 900) {
			// 	$('.abs_wrapper').css({'height' : $('.content').height() + 150})
			// } else {
			// 	$('.abs_wrapper').css({'height' : '100%'})
			// }

			
		})

		



	})




	$('.abs_wrapper').on('click', function(e) {

		$('.abs_profile__gallery').css({'display' : 'none'}).slick('unslick');
		$('.abs_wrapper').css({
			'display' : 'none'
		})

		$('.abs__abs').css({
			'display' : 'none'
		})
	})


	// PAGE:home (comments)
	$('a.comment').on('click', function(e) {
		var id = $(this).data('loop')
		$(`#comment-form${id}`).slideToggle()
		$(`#comment-form${id}`).find('#id_body').focus()

	})


	$('.content__news').slick({
		infinite: true,
		slidesToShow: 3,
		slidesToScroll: 1,
		vertical: true,
		verticalSwiping: true,
        touchThreshold: true,
        arrows: false,
        autoplay: true,
      	autoplaySpeed: 3500,
        
	})

	$('.content__news').on('wheel', (function(e) {
    e.preventDefault();

    clearTimeout(scroll);
    scroll = setTimeout(function(){scrollCount=0;}, 200);
    if(scrollCount) return 0;
    scrollCount=1;

    if (e.originalEvent.deltaY < 0) {
        $(this).slick('slickNext');
    } else {
        $(this).slick('slickPrev');
    }
}));


	// const list = document.querySelector('ul');
	// const cardCount = 52;

	// const createCard = () => {
	// 	const element = document.createElement('li');
	// 	const card = document.createElement('div');
	// 	card.className = 'card';
	// 	element.appendChild(card);
	// 	list.appendChild(element);
	// };

	// Array(cardCount).fill().forEach(() => createCard());
	// const cards = document.querySelectorAll('li');

	// const handleIntersection = (entries) => {
	// 	for (const entry of entries) {
	// 		entry.target.style.setProperty('--shown', entry.isIntersecting ? 1 : 0);
	// 	}
	// };

	// const observer = new IntersectionObserver(handleIntersection);
	// cards.forEach(card => observer.observe(card))





	







});