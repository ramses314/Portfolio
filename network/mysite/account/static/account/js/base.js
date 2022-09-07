
// $.ajax(
// 	'http://127.0.0.1:8000/',
// 	{
// 		success : function() {
// 			console.log(44);
// 		}
// 	}
// 	);




var b = $('.news__img')

console.log(44, b.offsetParent('.news'))


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

	$('.card__follow').on('click', function(e){
		let check = $('#follow-check').hasClass('sign');

		if (check) {
			$('#follow-check').removeClass('sign')
			$('#follow-check').addClass('unsign')
			$('#link-check').text('Подписаться')
		} else {
			$('#follow-check').removeClass('unsign')
			$('#follow-check').addClass('sign')
			$('#link-check').text('Отписаться')
		}
	})

});