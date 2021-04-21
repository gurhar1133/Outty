let cardFadeIn = anime({
  targets: '.card',
  opacity: ['0%', '100%'],
  translateY: [-20, 0],
  duration: 900,
  easing: 'easeOutElastic'
});

let suggestionEntrance = anime({
  targets: '.suggestion-card',
  opacity: ['0%', '100%'],
  translateY: [-20, 0],
  duration: 900,
  easing: 'easeOutElastic'
});


// let dashTextFadeIn = anime({
//   targets: '.dashboard-text',
//   opacity: ['0%', '100%'],
//   translateX: [-40, 0],
//   duration: 900,
//   easing: 'easeOutElastic'
//
// });

let dislikeAnimation = anime({
  targets: '.suggestion-card',
  opacity: ['100%', '0%'],
  translateY: [0, 3],
  rotate: [0, -5],
  duration: 400,
  easing: 'easeOutCubic',
  autoplay: false
});

let likeAnimation = anime({
  targets: '.suggestion-card',
  opacity: ['100%', '0%'],
  translateY: [0, 3],
  rotate: [0, 5],
  duration: 400,
  easing: 'easeOutCubic',
  autoplay: false
});

let completedAnimation = anime({
  targets: '.suggestion-card',
  opacity: ['100%', '0%'],
  translateY: [0, -20],
  duration: 400,
  easing: 'easeOutCubic',
  autoplay: false
});

let expandedCardAnimation = anime({
  targets: '.expanded-card',
  opacity: ['0%', '100%'],
  translateX: ['0em', '-10em'],
  duration: 500,
  easing: 'easeInOutCubic',
  autoplay: false,
  // direction:'alternate',
});

let expandedCardSuggestionAnimation = anime({
  targets: '.suggestion-card',
  // opacity: ['0%', '100%'],
  translateX: ['0em', '-10em'],
  duration: 500,
  easing: 'easeInOutCubic',
  autoplay: false,
  // direction:'alternate',
});

// let expandedCardGreetingAnimation = anime({
//   targets: '.dashboard-text',
//   opacity: ['100%', '0%'],
//   translateX: ['0em', '-30em'],
//   duration: 500,
//   easing: 'easeInOutCubic',
//   autoplay: false,
//   // direction:'alternate',
// });

let closeButtonAnimation = anime({
  targets: '.close-button',
  opacity: ['0%', '100%'],
  translateX: ['0em', '-10em'],
  duration: 500,
  easing: 'easeInOutCubic',
  autoplay: false,
});



let expandButton = document.getElementById('expand-button');
let dislikeButton = document.getElementById('dislike-button');
let completedButton = document.getElementById('completed-button');
let likeButton = document.getElementById('like-button');
let closeButton = document.getElementById('close-button');

dislikeButton.addEventListener('click', function(e) {
  dislikeAnimation.play();
  if (expandedCardGreetingAnimation.began) {
    toggle2();
  }
});

completedButton.addEventListener('click', function() {
  completedAnimation.play();
  if (expandedCardGreetingAnimation.began) {
    toggle2();
  }
});

likeButton.addEventListener('click', function() {
  likeAnimation.play();
  if (expandedCardGreetingAnimation.began) {
    toggle2();
  }
});


function toggle() {
  if (expandedCardGreetingAnimation.began) {
    expandedCardGreetingAnimation.reverse()
    expandedCardAnimation.reverse();
    expandedCardSuggestionAnimation.reverse();
    closeButtonAnimation.reverse();

    if (expandedCardGreetingAnimation.progress === 100 && expandedCardGreetingAnimation.direction === 'reverse') {
      expandedCardGreetingAnimation.completed = false
    }
  }

  if (expandedCardGreetingAnimation.paused) {
    expandedCardGreetingAnimation.play();
    expandedCardAnimation.play();
    expandedCardSuggestionAnimation.play();
    closeButtonAnimation.play();
  }
}

function toggle2() {
  if (expandedCardGreetingAnimation.direction === 'normal') {
    expandedCardGreetingAnimation.reverse()
    expandedCardAnimation.reverse();
    expandedCardSuggestionAnimation.reverse();
    closeButtonAnimation.reverse();

    if (expandedCardGreetingAnimation.progress === 100 && expandedCardGreetingAnimation.direction === 'reverse') {
      expandedCardGreetingAnimation.completed = false
    }

    if (expandedCardGreetingAnimation.paused) {
      expandedCardGreetingAnimation.play();
      expandedCardAnimation.play();
      expandedCardSuggestionAnimation.play();
      closeButtonAnimation.play();
    }
  }


}

expandButton.addEventListener('click', toggle);
closeButton.addEventListener('click', toggle);